#!/usr/bin/bash
#
# Some basic monitoring functionality; Tested on Amazon Linux 2
#
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
MEMORYUSAGE=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
PROCESSES=$(expr $(ps -A | grep -c .) - 1)
HTTPD_PROCESSES=$(ps -A | grep -c httpd)
CPUUSAGE=$(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)*100}')
DISKUSAGE=$(df -h / | awk 'NR==2{printf "%s", $5}')
LOADAVG=$(uptime | awk '{print $NF}')
NETWORK_TRAFFIC=$(sar -n DEV 1 1 | awk '/^Average/{print "rx: " $6 " KB/s", "tx: " $7 " KB/s"}')

echo -e "Instance ID: $INSTANCE_ID \n"
echo -e "Memory utilisation: $MEMORYUSAGE \n"
echo -e "No of processes: $PROCESSES \n"
echo -e "Disk usage: $DISKUSAGE \n"
echo -e "CPU usage: $CPUUSAGE \n"
if [ $HTTPD_PROCESSES -ge 1 ]
then
    echo -e "Web server is running \n"
else
    echo -e "Web server is NOT running \n"
fi
echo -e "Load average (5 min): $LOADAVG \n"
echo -e "Network traffic: $NETWORK_TRAFFIC \n"
