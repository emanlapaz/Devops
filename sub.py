import subprocess

keyname = 'keyname.pem'
ip_address = '11.22.33.44'

# Copy the monitor.sh script to the EC2 instance
subprocess.run(['scp', '-i', keyname, 'monitor.sh', f'ec2-user@{ip_address}:.'])

# Set the executable permissions on the script
subprocess.run(['ssh', '-i', keyname, f'ec2-user@{ip_address}', 'chmod', '700', 'monitor.sh'])

# Run the script on the EC2 instance and print the output to the terminal
result = subprocess.run(['ssh', '-i', keyname, f'ec2-user@{ip_address}', './monitor.sh'], capture_output=True, text=True)
print(result.stdout)
