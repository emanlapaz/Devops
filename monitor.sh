#!/usr/bin/bash
#
# Some basic monitoring functionality; Tested on Amazon Linux 2
#
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
MEMORYUSAGE=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
PROCESSES=$(expr $(ps -A | grep -c .) - 1)
HTTPD_PROCESSES=$(ps -A | grep -c httpd)

echo "Instance ID: $INSTANCE_ID"
echo "Memory utilisation: $MEMORYUSAGE"
echo "No of processes: $PROCESSES"
if [ $HTTPD_PROCESSES -ge 1 ]
then
    echo "Web server is running"
else
    echo "Web server is NOT running"
fi

##########################################################################
#!/usr/bin/bash
#
# Basic system monitoring script; tested on Amazon Linux 2
#

# Get instance ID
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)

# Get memory usage
MEMORY_USAGE=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')

# Get CPU usage
CPU_USAGE=$(mpstat 1 1 | awk '/Average:/ {print 100-$NF"%"}')

# Get number of processes
PROCESS_COUNT=$(expr $(ps -A | grep -c .) - 1)

# Get number of HTTPD processes
HTTPD_PROCESSES=$(ps -A | grep -c httpd)

# Get disk usage
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}')

# Print output
echo "Timestamp: $(date)"
echo "Instance ID: $INSTANCE_ID"
echo "Memory usage: $MEMORY_USAGE"
echo "CPU usage: $CPU_USAGE"
echo "Number of processes: $PROCESS_COUNT"
if [ $HTTPD_PROCESSES -ge 1 ]
then
    echo "Web server is running"
else
    echo "Web server is NOT running"
fi
echo "Disk usage: $DISK_USAGE"
