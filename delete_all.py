#!/usr/bin/env python3
import boto3

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    bucket.objects.all().delete()
    bucket.delete()

print("All S3 buckets emptied and deleted")

ec2 = boto3.resource('ec2')

for inst in ec2.instances.all():
    inst.terminate()

print("All instances terminated")