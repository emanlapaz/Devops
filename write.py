import boto3
bucket_name = 'jbloogs'
region= 'us_east'
EC2_url = 'ec2 test'
S3_url = "http://{bucket_name}.s3-website-{region}.amazonaws.com"


with open('test.txt', 'w') as f:
		f.write(f'EC2 instance URL: {EC2_url}\n')
		f.write(f'S3 bucket URL: {S3_url}\n')
			
with open('test.html', 'w') as f:
		f.write(f'<img src="http://{bucket_name}.s3-website-{region}.amazonaws.com">\n')