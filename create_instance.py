#!/usr/bin/env python3
import boto3
import webbrowser
import time
import sys
import random
import string
import urllib.request
from dateutil import parser


print("Create EC2 Instance")
ec2 = boto3.resource('ec2')
#user input instance name
instance_name = input("Instance name: ")
ami_id = 'ami-0dfcb1ef8550277af'
"""
# get the latest AMI id using Filters and sorted
filters = [{'Name': 'name', 'Values': ['amzn2-ami-hvm-*']}]
images = list(ec2.images.filter(Filters=filters).all())
latest_image = sorted(images, key=lambda x: x.creation_date, reverse=True)[0]
ami_id = latest_image.id
"""
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
			UserData="""#!/bin/bash
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