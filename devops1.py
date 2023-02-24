#!/usr/bin/env python3
import boto3
import webbrowser
import time
import sys
import random
import string
import urllib.request
from dateutil import parser


#######################################################################
#EC2 INSTANCE
#######################################################################
print("Create EC2 Instance")
ec2 = boto3.resource('ec2')
#user input instance name
instance_name = input("Instance name: ")

# get the latest AMI id using Filters and sorted
filters = [{'Name': 'name', 'Values': ['amzn2-ami-hvm-*']}]
images = list(ec2.images.filter(Filters=filters).all())
latest_image = sorted(images, key=lambda x: x.creation_date, reverse=True)[0]
ami_id = latest_image.id
print(f"The latest Amazon Linux 2 AMI ID is: {ami_id}")

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
	print("waiting for instance to run...")
	instance.wait_until_running()
	print(instance_name, instanceID, "Instance State is Running")

except:
	print("Error: unable to create Instance")

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
	instance.reload()

	# opens the web browser
	print("waiting for the user data update to finish.. please wait")
	time.sleep(30)
	webbrowser.open_new_tab(public_add)
	print("Web browser open at: ", public_add)
	instance.reload()

except: 
	print("Error: Unable to open web browser")

print("EC2 Instance created successfully\n")
#######################################################################
#S3 BUCKET:
#######################################################################
print("Create S3 Bucket")
#randomly selects 4 lowercase letter and digits
digits = random.choices(string.digits, k=3)
letters = random.choices(string.ascii_lowercase, k= 3)  
s3 = boto3.resource("s3")

#shuffles the letters and digits and generates a random bucket name
name= random.sample(digits + letters, 6)
bucket_name = "jbloggs" + ''.join(name)
print("Unique bucket name generated: " + bucket_name)

# create bucket
try:
	s3.create_bucket(Bucket=bucket_name)
	print("S3 Bucket created:", bucket_name)
except:
	print ("Error: unable to create s3 bucket", bucket_name)



# url to download image
url_src = "http://devops.witdemo.net/logo.jpg"

# output path of the downloaded file
output_path = "/home/eugene/Devops/images/image.jpg"

# downloads the file
urllib.request.urlretrieve(url_src, output_path)
print("image downloaded from:", url_src)



# function to upload the image to bucket, make it public, and open the web browser to display the image
try:
	def upload_to_bucket():
		# initialize S3 client
		s3 = boto3.client('s3')

		# set the bucket name and image file name
		s3_bucket = bucket_name
		wit_logo = 'image.jpg'
		index = 'index.html'
		region = 'us-east-1'

		# upload the image to the bucket and make it public
		s3.upload_file(wit_logo, s3_bucket, wit_logo, ExtraArgs={'ContentType': 'image/jpeg'})
		s3.put_object_acl(Bucket=s3_bucket, Key=wit_logo , ACL='public-read')
		print("uploaded:", wit_logo)
		s3.upload_file(index, s3_bucket, index, ExtraArgs={'ContentType': 'text/html'})
		s3.put_object_acl(Bucket=s3_bucket, Key=index , ACL='public-read')
		print("uploaded:", index)

		# open the image in the default web browser
		uploaded_url = f"http://{bucket_name}.s3-website-{region}.amazonaws.com"
		webbrowser.open(uploaded_url)
		
		# print the uploaded url
		print("Amazon S3 URL for the uploaded website:", uploaded_url)


	upload_to_bucket()

except: 
	print("Error: Failed to upload to bucket")

try:
	#website configuration
	website_configuration = {
		'ErrorDocument': {'Key': 'error.html'},
		'IndexDocument': {'Suffix':'index.html'},
	}

	bucket_website = s3.BucketWebsite(bucket_name)
	response = bucket_website.put(WebsiteConfiguration=website_configuration)
except:
	print("Error: Web configuration")

print("S3 Bucket created successfully\n")

####################################################################




"""
Sources/References:
to dos:
"""
