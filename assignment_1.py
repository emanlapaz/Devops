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
#EC2 instance
#######################################################################

ec2 = boto3.resource('ec2')
#user input instance name
instance_name = input("Instance name: ")

#updated AMI id
filters = [{'Name': 'name', 'Values': ['amzn2-ami-hvm-*']}]
images = list(ec2.images.filter(Filters=filters).all())
latest_image = sorted(images, key=lambda x: x.creation_date, reverse=True)[0]
ami_id = latest_image.id
print(f"The latest Amazon Linux 2 AMI ID is: {ami_id}")


new_instances = ec2.create_instances(
		ImageId=ami_id,
		MinCount=1,
		MaxCount=1,
		InstanceType='t2.nano',
		KeyName='kp',
		SecurityGroups=['launch-wizard-1'],
		UserData=
			"""#!/bin/bash
			yum install httpd -y
			systemctl enable httpd
			systemctl start httpd""",
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
print("Instance state: Running", instance_name, instanceID)

instance.reload()

# function to return the Public Ip Address
#source: https://www.learnaws.org/2020/12/16/aws-ec2-boto3-ultimate-guide/
def get_public_ip(instanceID):
	ec2_client = boto3.client('ec2')
	reservations = ec2_client.describe_instances(InstanceIds=[instanceID]).get("Reservations")

	for reservation in reservations:
		for instance in reservation['Instances']:
			return instance.get("PublicIpAddress")

public_add = get_public_ip(instanceID)
instance.reload()

#######################################################################
#S3 bucket:
#######################################################################

#randomly selects 4 lowercase letter and digits
digits = random.choices(string.digits, k=3)
letters = random.choices(string.ascii_lowercase, k= 3)  
s3 = boto3.resource("s3")
#shuffles the letters and digits and generates a random bucket name
name= random.sample(digits + letters, 6)
bucket_name = "jbloggs" + ''.join(name)
print("Unique bucket name generated: " + bucket_name)

#create bucket
s3.create_bucket(Bucket=bucket_name)
print("S3 Bucket created:", bucket_name)


website_configuration = {
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}

bucket_website = s3.BucketWebsite(bucket_name)
response = bucket_website.put(WebsiteConfiguration=website_configuration)


#print to terminal
print("Upload an index.html file to test it works!" )
print("waiting for the web browser to open.. please wait")
time.sleep(30)
webbrowser.open_new_tab(public_add)
print("Web Browser Open at", public_add)
instance.reload()


