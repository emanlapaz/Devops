#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta
import time

cloudwatch = boto3.resource('cloudwatch')
ec2 = boto3.resource('ec2')

instid = input("Please enter instance ID: ")    # Prompt the user to enter an Instance ID
instance = ec2.Instance(instid)

instance.monitor()  # Enables detailed monitoring on instance (1-minute intervals)
   # Wait 6 minutes to ensure we have some data (can remove if not a new instance)

proceed = input("Do you want to proceed with CloudWatch monitoring? (yes/no) ")

if proceed.lower() == "yes":
    print("wait for 6 minutes to ensure data collection")
    time.sleep(360)  
    # Retrieve CPU utilization metric
    cpu_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
                                              MetricName='CPUUtilization',
                                              Dimensions=[{'Name':'InstanceId', 'Value': instid}])

    cpu_metric = list(cpu_iterator)[0]    # extract first (only) element
    cpu_response = cpu_metric.get_statistics(StartTime = datetime.utcnow() - timedelta(minutes=5),   # 5 minutes ago
                                              EndTime=datetime.utcnow(),                              # now
                                              Period=300,                                             # 5 min intervals
                                              Statistics=['Average'])

    # Retrieve NetworkIn metric
    networkin_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
                                                    MetricName='NetworkIn',
                                                    Dimensions=[{'Name':'InstanceId', 'Value': instid}])

    networkin_metric = list(networkin_iterator)[0]    # extract first (only) element
    networkin_response = networkin_metric.get_statistics(StartTime = datetime.utcnow() - timedelta(minutes=5),   # 5 minutes ago
                                                          EndTime=datetime.utcnow(),                              # now
                                                          Period=300,                                             # 5 min intervals
                                                          Statistics=['Average'])

    # Retrieve NetworkOut metric
    networkout_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
                                                     MetricName='NetworkOut',
                                                     Dimensions=[{'Name':'InstanceId', 'Value': instid}])

    networkout_metric = list(networkout_iterator)[0]    # extract first (only) element
    networkout_response = networkout_metric.get_statistics(StartTime = datetime.utcnow() - timedelta(minutes=5),   # 5 minutes ago
                                                            EndTime=datetime.utcnow(),                              # now
                                                            Period=300,                                             # 5 min intervals
                                                            Statistics=['Average'])

    # Print out the results
    print(f"Instance ID: {instid}")
    print(f"Average CPU utilization: {cpu_response['Datapoints'][0]['Average']} {cpu_response['Datapoints'][0]['Unit']}")
    print(f"Average NetworkIn: {networkin_response['Datapoints'][0]['Average']} {networkin_response['Datapoints'][0]['Unit']}")
    print(f"Average NetworkOut: {networkout_response['Datapoints'][0]['Average']} {networkout_response['Datapoints'][0]['Unit']}")
    
elif proceed.lower() == "no":
    print("Exiting program.")
else:
    print("Please answer with 'yes' or 'no'.")
