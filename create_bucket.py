#!/usr/bin/env python3
import boto3
import random
import string
import urllib.request
import webbrowser

digits = random.choices(string.digits, k=3)
letters = random.choices(string.ascii_lowercase, k= 3)  
s3 = boto3.resource("s3")

name= random.sample(digits + letters, 6)

bucket_name = "jbloggs" + ''.join(name)

s3.create_bucket(Bucket=bucket_name)

print("Unique bucket name: " + bucket_name)



#url to download image
url = "http://devops.witdemo.net/logo.jpg"
#output path to images folder
output_path = "/home/eugene/Public/image.jpg"
urllib.request.urlretrieve(url, output_path)
print("image downloaded from:", url)

#uploading image to bucket

import webbrowser

def upload_to_bucket():
    # initialize S3 client
    s3 = boto3.client('s3')

    # set the bucket name and image file name
    s3_buck = bucket_name
    wit_logo = 'image.jpg'
    index = 'index.html'
    region = 'us-east-1'

    # upload the image to the bucket and make it public
    s3.upload_file(wit_logo, s3_buck, wit_logo, ExtraArgs={'ContentType': 'image/jpeg'})
    s3.put_object_acl(Bucket=s3_buck, Key=wit_logo , ACL='public-read')
    print("upload 1 done")
    s3.upload_file(index, s3_buck, index, ExtraArgs={'ContentType': 'text/html'})
    s3.put_object_acl(Bucket=s3_buck, Key=index , ACL='public-read')
    print("upload 2 done")

    # open the image in the default web browser
    url = f"http://{bucket_name}.s3-website-{region}.amazonaws.com/{wit_logo}"
    webbrowser.open(url)


website_configuration = {
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}

bucket_website = s3.BucketWebsite(bucket_name)
response = bucket_website.put(WebsiteConfiguration=website_configuration)


amazon_url = upload_to_bucket()
print("Amazon S3 URL for the uploaded image:", amazon_url)