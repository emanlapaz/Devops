import boto3
ec2 = boto3.resource('ec2')

#user input instance name
instance_name = input("Instance name: ")

#filter source: https://stackoverflow.com/questions/51611411/get-latest-ami-id-for-aws-instance
def get_latest_imageId():

	ec2 = boto3.client('ec2')

	response = ec2.describe_images(
		Filters=[{
                'Name': 'name',
                'Values': ['amzn-ami-hvm-*']
            },{
                'Name': 'description',
                'Values': ['Amazon Linux AMI*']
            },{
                'Name': 'architecture',
                'Values': ['x86_64']
            },{
                'Name': 'owner-alias',
                'Values': ['amazon']
            },{
                'Name': 'owner-id',
                'Values': ['137112412989']
            },{
                'Name': 'state',
                'Values': ['available']
            },{
                'Name': 'root-device-type',
                'Values': ['ebs']
            },{
                'Name': 'virtualization-type',
                'Values': ['hvm']
            },{
                'Name': 'hypervisor',
                'Values': ['xen']
            },{
                'Name': 'image-type',
                'Values': ['machine']
            } ]
	)
		
	latest_image_id = response['Images'][0]['ImageId']
	print(f"The latest Amazon Linux 2 AMI ID is: {latest_image_id}")
	return latest_image_id
	
latest_image = get_latest_imageId()
print(latest_image)


new_instances = ec2.create_instances(
		ImageId= latest_image,
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
		
print ('New instance created: ', instance_name, instanceID)

