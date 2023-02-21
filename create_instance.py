import boto3
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
				'Tags': [{'Key': 'Name','Value': 'WebServer'}]
			}]
		)

instanceID=(new_instances[0].id)					
		
print ("Creating new instance:")
print (instanceID)

