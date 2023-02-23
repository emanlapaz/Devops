#!/usr/bin/env python3
import boto3
ec2 = boto3.resource('ec2')

#user input instance name
instance_name = input("Instance name: ")

new_instances = ec2.create_instances(
		ImageId= 'ami-0dfcb1ef8550277af',
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

instanceID=(new_instances[0].id)
instance = ec2.Instance(instanceID)

#ip = instanceID.public_ip_address

		
print ('New instance created: ', instance_name, instanceID)

