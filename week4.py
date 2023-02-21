import boto3
import webbrowser
import time
import sys
import random
import string

#EC2 instance
ec2 = boto3.resource('ec2')

new_instances = ec2.create_instances(
		ImageId='ami-0aa7d40eeae50c9a9',
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
				'Tags': [{'Key': 'Name','Value': 'Week4'}]
			}]
		)

instanceID = (new_instances[0].id)
instance = ec2.Instance(instanceID)
instance.wait_until_running()

# function to return the Public Ip Address
#source: https://www.learnaws.org/2020/12/16/aws-ec2-boto3-ultimate-guide/
def get_public_ip(instanceID):
	ec2_client = boto3.client('ec2')
	reservations = ec2_client.describe_instances(InstanceIds=[instanceID]).get("Reservations")

	for reservation in reservations:
		for instance in reservation['Instances']:
			return instance.get("PublicIpAddress")

public_add = get_public_ip(instanceID)

#S3 bucket:

#randomly selects 4 lowercase letter and digits
digits = random.choices(string.digits, k=4)
letters = random.choices(string.ascii_lowercase, k= 4)  
s3 = boto3.resource("s3")

#shuffles the letters and digits
name= random.sample(digits + letters, 8)

bucket_name = "bucket" + ''.join(name)

s3.create_bucket(Bucket=bucket_name)
website_configuration = {
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}

bucket_website = s3.BucketWebsite(bucket_name)
response = bucket_website.put(WebsiteConfiguration=website_configuration)


#print to terminal
print("Your instance is up and running")
print ("New instance created:"+instanceID, "Public Address:",public_add)
print("Unique bucket name: " + bucket_name)
print("Upload an index.html file to test it works!" )
time.sleep(30)
webbrowser.open_new_tab(public_add)
print("Web Browser Open")


