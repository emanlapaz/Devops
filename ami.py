import boto3

client = boto3.client('ec2')

response = client.describe_images(
    Filters=[
        {'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']},
        {'Name': 'owner-id', 'Values': ['amazon']},
        {'Name': 'state', 'Values': ['available']}
    ],
    DryRun=False,
    MaxResults=1000 # increase the number of results to retrieve
)

images = response['Images']
images.sort(key=lambda x: x['CreationDate'], reverse=True)

ami_id = images[0]['ImageId']

print("The latest Amazon Linux 2 AMI ID is: ", ami_id)
