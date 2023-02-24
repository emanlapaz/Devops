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
url_src = "http://devops.witdemo.net/logo.jpg"
#output path to images folder
output_path = "/home/eugene/Public/image.jpg"
urllib.request.urlretrieve(url_src, output_path)
print("image downloaded from:", url_src)

#uploading image to bucket

import webbrowser

def upload_to_bucket():
    # initialize S3 client
    s3 = boto3.client('s3')

    # set the bucket name and image file name
    s3_bucket = bucket_name
    wit_logo = 'image.jpg'
    index = 'index.html'
    region = 'us-east-1'

    # upload the image to the bucket and make it public
    s3.upload_file(wit_logo, s3_bucket, wit_logo, ExtraArgs={'ContentType': 'image/jpeg'})
    s3.put_object_acl(Bucket=s3_bucket, Key=wit_logo , ACL='public-read')
    print("upload 1 done")
    s3.upload_file(index, s3_bucket, index, ExtraArgs={'ContentType': 'text/html'})
    s3.put_object_acl(Bucket=s3_bucket, Key=index , ACL='public-read')
    print("upload 2 done")


    # open the image in the default web browser
    uploaded_url = f"http://{bucket_name}.s3-website-{region}.amazonaws.com"
    webbrowser.open(uploaded_url)
    #print the uploaded url
    print("Amazon S3 URL for the uploaded image:", uploaded_url)


website_configuration = {
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix':'index.html'},
}

bucket_website = s3.BucketWebsite(bucket_name)
response = bucket_website.put(WebsiteConfiguration=website_configuration)

upload_to_bucket()