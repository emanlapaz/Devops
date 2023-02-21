import boto3
import webbrowser
import time
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

#print to terminal
print("Your instance is up and running")
print ("New instance created:"+instanceID)
print("Public Address:",public_add)
time.sleep(30)
webbrowser.open_new_tab(public_add)
print("Web Browser Open")


