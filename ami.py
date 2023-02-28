import boto3

ec2 = boto3.resource('ec2')

image_id = 'ami-0dfcb1ef8550277af'

image = ec2.Image(image_id)

if not image:
    print(f"No matching AMI found with ID {image_id}")
else:
    print(f"Selected AMI: {image.id}")
