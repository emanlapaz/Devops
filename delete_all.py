#!/usr/bin/env python3
import boto3

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    if bucket.name != 'jbloggs0pn73a':
        bucket.objects.all().delete()
        bucket.delete()

print("All S3 buckets except jbloggs0pn73a emptied and deleted")

ec2 = boto3.resource('ec2')

for inst in ec2.instances.all():
    inst.terminate()

print("All instances terminated")
