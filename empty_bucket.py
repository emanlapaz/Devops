#!/usr/bin/env python3
import boto3

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    bucket.objects.all().delete()
    bucket.delete

print("Bucket empty")