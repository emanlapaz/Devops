#!/usr/bin/env python3
import boto3
ec2 = boto3.resource('ec2')

for inst in ec2.instances.all():
    inst.terminate()

print("All instances terminated")