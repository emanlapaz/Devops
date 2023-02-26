#!/usr/bin/env python3
import boto3
import webbrowser
import time
import sys
import random
import string
import urllib.request
from dateutil import parser
from datetime import datetime, timedelta

#randomly selects 4 lowercase letter and digits
digits = random.choices(string.digits, k=3)
letters = random.choices(string.ascii_lowercase, k= 3) 
name= random.sample(digits + letters, 6)


#######################################################################
#EC2 INSTANCE
#######################################################################
print("CREATE EC2 INSTANCE\n")
ec2 = boto3.resource('ec2')
#creates a random instance name tag
instance_name = "EC2" + ''.join(name)
print(f"Random EC2 instance name tag generated: {instance_name}\n")

# get the latest AMI id using Filters and sorted
print("Checking for the latest AMI ID\n")
filters = [{'Name': 'name', 'Values': ['amzn2-ami-hvm-*']}]
images = list(ec2.images.filter(Filters=filters).all())
latest_image = sorted(images, key=lambda x: x.creation_date, reverse=True)[0]
ami_id = latest_image.id
print(f"The latest Amazon Linux 2 AMI ID is: {ami_id}\n")

# creates a new instance
try:
	new_instances = ec2.create_instances(
			ImageId=ami_id,
			MinCount=1,
			MaxCount=1,
			InstanceType='t2.nano',
			KeyName='kp',
			SecurityGroups=['launch-wizard-1'],
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
	

except:
	print("Error: unable to create Instance\n")

instance.reload()

try:
	# function to return the Public Ip Address
	def get_public_ip(instanceID):
		ec2_client = boto3.client('ec2')
		reservations = ec2_client.describe_instances(InstanceIds=[instanceID]).get("Reservations")

		for reservation in reservations:
			for instance in reservation['Instances']:
				return instance.get("PublicIpAddress")

	public_add = get_public_ip(instanceID)
	print(f"Instance public address: {public_add}\n")
	instance.reload()

	# opens the web browser
	print("waiting for the user data update to finish.. please wait\n")
	time.sleep(30)
	instance.reload()

except: 
	print("Error: Unable to open web browser\n")

print("EC2 Instance created successfully\n")

#######################################################################
#S3 BUCKET:
#######################################################################
print("CREATE S3 BUCKET\n")

region = 'us-east-1'
s3 = boto3.resource("s3")

#shuffles the letters and digits and generates a random bucket name
bucket_name = "jbloggs" + ''.join(name)

print(f"Unique bucket name generated: {bucket_name}\n")

# create bucket
try:
	s3.create_bucket(Bucket=bucket_name)
	print(f"S3 Bucket created: {bucket_name}\n")
except:
	print ("Error: unable to create s3 bucket")



# url to download image
url_src = "http://devops.witdemo.net/logo.jpg"
output_path = "/home/eugene/Devops/images/image.jpg"
wit_logo = 'image.jpg'
index = 'index.html'
# downloads the file
urllib.request.urlretrieve(url_src, output_path)
print(f"image downloaded from: {url_src}\n")


# function to upload the image to bucket, make it public, and open the web browser to display the image
try:
	def upload_to_bucket():
		# initialize S3 client
		s3 = boto3.client('s3')
		s3_bucket = bucket_name
		
		

		# upload the image to the bucket and make it public
		s3.upload_file(wit_logo, s3_bucket, wit_logo, ExtraArgs={'ContentType': 'image/jpeg','ACL':'public-read'})
		#s3.put_object_acl(Bucket=s3_bucket, Key=wit_logo , ACL='public-read')
		print(f"uploaded: {wit_logo}\n")
		s3.upload_file(index, s3_bucket, index, ExtraArgs={'ContentType': 'text/html', 'ACL':'public-read'})
		#s3.put_object_acl(Bucket=s3_bucket, Key=index , ACL='public-read')
		print(f"uploaded: {index}\n")

		object_url = f'https://{s3_bucket}.s3.amazonaws.com/{wit_logo}'

		with open('index.html', 'w') as f:
			f.write(f'<img src="{object_url}">')
		print("wit logo object bucket url added to index.html\n")
		

	upload_to_bucket()

except: 
	print("Error: Failed to upload to bucket")



print(f"S3 Bucket {bucket_name}created successfully\n")

###################################################################
#Open browser
##################################################################

#web browser urls
instance_url = f'http://{public_add}'
s3_url = f"http://{bucket_name}.s3-website-{region}.amazonaws.com"

#add the urls to a txt file name eugeneurls
try:
	with open('eugeneurls.txt', 'w') as f:
		f.write(f'EC2 instance URL: {instance_url}\n')
		f.write(f'S3 bucket URL: {s3_url}\n')
		
		print(f"{s3_url} added to eugeneurls.txt\n")
		print(f"{instance_url} added to eugeneurls.txt\n")
except:
	print("Error: Unable to write to file")

try:
	#website configuration
	print("Configuring website\n")
	website_configuration = {
		'ErrorDocument': {'Key': 'error.html'},
		'IndexDocument': {'Suffix':'index.html'},
	}

	bucket_website = s3.BucketWebsite(bucket_name)
	response = bucket_website.put(WebsiteConfiguration=website_configuration)
except:
	print("Error: Web configuration")

#opening web browsers
try:
	print(f"Opening EC2 website at {instance_url}\n")
	webbrowser.open_new_tab(public_add)
	print(f"Opening S3 website at {s3_url}\n")
	webbrowser.open_new_tab(s3_url)
	print("Web sites open\n")
except:
	print("Error: Failed to open websites\n")
####################################################################
#Cloudwatch
####################################################################

print("WARNING: Cloudwatch takes 6 minutes to ensure data collection for new Instances")
proceed = input("Do you want to proceed with CloudWatch monitoring? (yes/no)\n ")
cloudwatch = boto3.resource('cloudwatch')
ec2 = boto3.resource('ec2')
instance = ec2.Instance(instanceID)

instance.monitor()  # Enables detailed monitoring on instance (1-minute intervals)
   # Wait 6 minutes to ensure we have some data (can remove if not a new instance)



if proceed.lower() == "yes":
    print(f"Starting CLOUDWATCH for {instance_name} {instanceID}\n")
    print("wait for 6 minutes to ensure data collection\n")
    time.sleep(360)  
    # Retrieve CPU utilization metric
    cpu_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
                                              MetricName='CPUUtilization',
                                              Dimensions=[{'Name':'InstanceId', 'Value': instanceID}])

    cpu_metric = list(cpu_iterator)[0]    # extract first (only) element
    cpu_response = cpu_metric.get_statistics(StartTime = datetime.utcnow() - timedelta(minutes=5),   # 5 minutes ago
                                              EndTime=datetime.utcnow(),                              # now
                                              Period=300,                                             # 5 min intervals
                                              Statistics=['Average'])

    # Retrieve NetworkIn metric
    networkin_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
                                                    MetricName='NetworkIn',
                                                    Dimensions=[{'Name':'InstanceId', 'Value': instanceID}])

    networkin_metric = list(networkin_iterator)[0]    # extract first (only) element
    networkin_response = networkin_metric.get_statistics(StartTime = datetime.utcnow() - timedelta(minutes=5),   # 5 minutes ago
                                                          EndTime=datetime.utcnow(),                              # now
                                                          Period=300,                                             # 5 min intervals
                                                          Statistics=['Average'])

    # Retrieve NetworkOut metric
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
    print(f"Average CPU utilization: {cpu_response['Datapoints'][0]['Average']} {cpu_response['Datapoints'][0]['Unit']}")
    print(f"Average NetworkIn: {networkin_response['Datapoints'][0]['Average']} {networkin_response['Datapoints'][0]['Unit']}")
    print(f"Average NetworkOut: {networkout_response['Datapoints'][0]['Average']} {networkout_response['Datapoints'][0]['Unit']}")
    
elif proceed.lower() == "no":
    print("Exiting program.")
else:
    print("Please answer with 'yes' or 'no'.")



"""
Sources/References:
to dos:
"""
