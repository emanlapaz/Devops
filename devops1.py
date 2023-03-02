#!/usr/bin/env python3
#eugenio_manlapaz

import boto3
import webbrowser
import time
import sys
import random
import string
import urllib.request
from dateutil import parser
from datetime import datetime, timedelta
import os
import subprocess

#randomly selects 4 lowercase letter and digits
digits = random.choices(string.digits, k=3)
letters = random.choices(string.ascii_lowercase, k= 3) 
name= random.sample(digits + letters, 6)

###############################
print("CREATING EC2 INSTANCE\n")

ec2 = boto3.resource('ec2')
#creates a random instance name tag
instance_name = "EC2" + ''.join(name)
print(f"Random EC2 instance name tag generated: {instance_name}\n")

ami_id = 'ami-0dfcb1ef8550277af'
keypair = 'kp'
security_name = 'launch-wizard-1'
inst_type = 't2.nano'
keyname = 'kp.pem'

#to do Filter up to date AMI ID

# creates a new instance
try:
	new_instances = ec2.create_instances(
			ImageId=ami_id,
			MinCount=1,
			MaxCount=1,
			InstanceType=inst_type,
			KeyName=keypair,
			SecurityGroups=[security_name],
			UserData="""
						#!/bin/bash
						yum install httpd -y
						systemctl enable httpd
						systemctl start httpd
						echo '<html>' > index.html
						echo 'Hello! This is my deployed website: ' >> index.html
						echo '<br>' >> index.html
						echo 'Instance Name: ' >> index.html
						curl http://169.254.169.254/latest/meta-data/hostname >> index.html
						echo '<br>' >> index.html
						echo 'Instance ID: ' >> index.html
						curl http://169.254.169.254/latest/meta-data/instance-id >> index.html
						echo '<br>' >> index.html
						echo 'Instance Type: ' >> index.html
						curl http://169.254.169.254/latest/meta-data/instance-type >> index.html
						echo '<br>' >> index.html
						echo 'AMI ID: ' >> index.html
						curl http://169.254.169.254/latest/meta-data/ami-id >> index.html
						echo '<br>' >> index.html
						echo 'Public IP address: ' >> index.html
						curl http://169.254.169.254/latest/meta-data/public-ipv4 >> index.html
						echo '<br>' >> index.html
						echo 'Private IP address: ' >> index.html
						curl http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html
						echo '<br>' >> index.html
						echo 'URLs saved in eugeneurls.txt file'
						cp index.html /var/www/html/index.html
						""",
			TagSpecifications=[
				{
					'ResourceType': 'instance',
					'Tags': [{'Key': 'Name','Value': instance_name}]
				}]
			)
	
	instanceID = (new_instances[0].id)
	instance = ec2.Instance(instanceID)
	print(f"Created new instance: {instance_name}\n")
	print(f"Instance ID: {instanceID}\n")
	print("waiting for instance to run...\n")
	instance.wait_until_running()
	print(f"{instance_name} is Running\n")
	

except Exception as e:
    print('Error: unable to create Instance-', str(e))

instance.reload()

try:
	#get the public ip address
	public_add = instance.public_ip_address
	print(f"Instance public address: {public_add}\n")
	instance.reload()

	# opens the web browser
	print("waiting for the user data update to finish.. please wait\n")
	time.sleep(30)
	instance.reload()

except Exception as e:
    print('Error: Unable to open web browser-', str(e))

print(F"EC2 Instance {instanceID} created successfully\n")

##############################
print("CREATING S3 BUCKET\n")

region = 'us-east-1'
s3 = boto3.resource("s3")

#shuffles the letters and digits and generates a random bucket name
bucket_name = "jbloggs" + ''.join(name)

# create bucket
try:
	s3.create_bucket(Bucket=bucket_name)
	print(f"S3 Bucket created: {bucket_name}\n")
	
except Exception as e:
    print('Error: unable to create s3 bucket-', str(e))


# url to download image
url_src = "http://devops.witdemo.net/logo.jpg"
output_path = "/home/eugene/Devops/image.jpg"
wit_logo = 'image.jpg'
index = 'index.html'
object_url = f'https://{bucket_name}.s3.amazonaws.com/{wit_logo}'

# downloads the file
urllib.request.urlretrieve(url_src, output_path)
print(f"image downloaded from: {url_src}\n")


# function to upload the image to bucket and make it public
try:
	def upload_to_bucket():
		# initialize S3 client
		s3 = boto3.client('s3')
		
		# upload the wit logo to the bucket and make it public
		s3.upload_file(wit_logo, bucket_name, wit_logo, ExtraArgs={'ContentType': 'image/jpeg','ACL':'public-read'})
		print(f"uploaded: {wit_logo}\n")

		# creates index.html if file not found and write the object url in the index.html file
		if not os.path.isfile('index.html'):
			with open('index.html', 'w') as f:
				f.write(f'<img src="{object_url}">')

		# uploads the index.html file to the bucket
		s3.upload_file(index, bucket_name, index, ExtraArgs={'ContentType': 'text/html', 'ACL':'public-read'})
		print(f"uploaded: {index}\n")

	upload_to_bucket()

except Exception as e:
    print('Error: Failed to upload to bucket-', str(e))

print(f"S3 Bucket {bucket_name}created successfully\n")

#web browser urls
instance_url = f'http://{public_add}'
s3_url = f"http://{bucket_name}.s3-website-{region}.amazonaws.com"

# adds the urls to a txt file named eugeneurls.txt
try:
	# creates eugeneurls if file is not found and writes the instance and s3 url
	if not os.path.isfile('eugeneurls.txt'):
		with open('eugeneurls.txt', 'w') as f:
			f.write(f'EC2 instance URL: {instance_url}\n')
			f.write(f'S3 bucket URL: {s3_url}\n')
		
	print(f"{s3_url} added to eugeneurls.txt\n")
	print(f"{instance_url} added to eugeneurls.txt\n")

except Exception as e:
    print('Error: Unable to write to file-', str(e))

try:
	# website configuration
	print("Configuring website\n")
	website_configuration = {
		'ErrorDocument': {'Key': 'error.html'},
		'IndexDocument': {'Suffix':'index.html'},
	}

	bucket_website = s3.BucketWebsite(bucket_name)
	response = bucket_website.put(WebsiteConfiguration=website_configuration)

except Exception as e:
    print('Error: Web configuration-', str(e))
    
#opening web browsers
try:
	print(f"Opening EC2 website at {instance_url}\n")
	webbrowser.open_new_tab(public_add)
	print(f"Opening S3 website at {s3_url}\n")
	webbrowser.open_new_tab(s3_url)
	print("Web sites open\n")

except Exception as e:
    print('Error: Failed to open websites-', str(e))
    
#Cloudwatch and monitoring.sh
####################################################################

proceed = input("Do you want to proceed with MONITORING (Cloudwatch and Monitoring.sh)? (yes/no)")
print("WARNING: Cloudwatch takes 6 minutes to ensure data collection for new Instances\n")


cloudwatch = boto3.resource('cloudwatch')
ec2 = boto3.resource('ec2')
instance = ec2.Instance(instanceID)

try:
	instance.monitor()  # Enables detailed monitoring on instance (1-minute intervals)
	# Wait 6 minutes to ensure we have some data (can remove if not a new instance)

	if proceed.lower() == "yes":
		print(f"Starting CLOUDWATCH for {instance_name} {instanceID}\n")
		print("wait for 6 minutes to ensure data collection\n")
		print("use Ctrl+C to discontinue monitoring\n")
		time.sleep(360)  
		#CPU utilization metric 
		cpu_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
												MetricName='CPUUtilization',
												Dimensions=[{'Name':'InstanceId', 'Value': instanceID}])

		cpu_metric = list(cpu_iterator)[0]
		cpu_response = cpu_metric.get_statistics(StartTime = datetime.utcnow() - timedelta(minutes=5),   # 5 minutes ago
												EndTime=datetime.utcnow(),                              # now
												Period=300,                                             # 5 min intervals
												Statistics=['Average'])

		# NetworkIn metric
		networkin_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
														MetricName='NetworkIn',
														Dimensions=[{'Name':'InstanceId', 'Value': instanceID}])

		networkin_metric = list(networkin_iterator)[0]    # extract first (only) element
		networkin_response = networkin_metric.get_statistics(StartTime = datetime.utcnow() - timedelta(minutes=5),   # 5 minutes ago
															EndTime=datetime.utcnow(),                              # now
															Period=300,                                             # 5 min intervals
															Statistics=['Average'])

		#NetworkOut metric
		networkout_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
														MetricName='NetworkOut',
														Dimensions=[{'Name':'InstanceId', 'Value': instanceID}])

		networkout_metric = list(networkout_iterator)[0]    # extract first (only) element
		networkout_response = networkout_metric.get_statistics(StartTime = datetime.utcnow() - timedelta(minutes=5),   # 5 minutes ago
																EndTime=datetime.utcnow(),                              # now
																Period=300,                                             # 5 min intervals
																Statistics=['Average'])

		# Print out the results
		print("Here are the results: \n")
		print("CLOUDWATCH:\n")
		print(f"Average CPU utilization: {cpu_response['Datapoints'][0]['Average']} {cpu_response['Datapoints'][0]['Unit']}\n")
		print(f"Average NetworkIn: {networkin_response['Datapoints'][0]['Average']} {networkin_response['Datapoints'][0]['Unit']}\n")
		print(f"Average NetworkOut: {networkout_response['Datapoints'][0]['Average']} {networkout_response['Datapoints'][0]['Unit']}\n")
		
	elif proceed.lower() == "no":
		print("Exiting program.")
	else:
		print("Invalid input: Exiting Program")
		sys.exit()

except Exception as e:
    print('Error: Cloudwatch failed- ', str(e))


#Monitor.sh

script = 'monitor.sh'

try:
    print("MONITOR.SH")
    # Copies the monitor.sh script to the EC2 instance via secure copy
    subprocess.run(['scp', '-o', 'StrictHostKeyChecking=no','-i', keyname, script, f'ec2-user@{public_add}:.'])

    # Adds the executable permissions on the monitor.sh
    subprocess.run(['ssh', '-i', keyname, f'ec2-user@{public_add}', 'chmod', '+x', script])

    # Runs the monitor.sh on the EC2 instance and print the output to the terminal
    result = subprocess.run(['ssh', '-i', keyname, f'ec2-user@{public_add}', './monitor.sh'], capture_output=True, text=True)
    print(result.stdout)

except Exception as e:
    print('Error: Monitoring failed - ', str(e))

"""
Sources/References:
1. Boto 3 - https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
2. EC2 - https://docs.aws.amazon.com/ec2/
3. S3 - https://docs.aws.amazon.com/s3/index.html
4. Cloudwatch - https://docs.aws.amazon.com/cloudwatch/index.html
5. Metadata service on AWS EC2- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html
6. User Data Ec2 - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html
7. webbrowser python module - https://docs.python.org/3/library/webbrowser.html
8. Python imports -  https://docs.python.org/3/library
9. Subprocess.run - https://stackoverflow.com/questions/89228/calling-an-external-command-in-python/89243#89243

To dos: get the updated AMI ID using Filters
"""
