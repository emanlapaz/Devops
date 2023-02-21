#!/usr/bin/env python3
import boto3
import random
import string

digits = random.choices(string.digits, k=4)
letters = random.choices(string.ascii_lowercase, k= 5)  
s3 = boto3.resource("s3")

name= random.sample(digits + letters, 9)

bucket_name = "bucket" + ''.join(name)

s3.create_bucket(Bucket=bucket_name)

print("Unique bucket name: " + bucket_name)
