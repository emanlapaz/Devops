#!/usr/bin/env python3
import boto3

ec2 = boto3.resource('ec2')
#user input instance name

#updated AMI id
filters = [{'Name': 'name', 'Values': ['amzn2-ami-hvm-*']}]
images = list(ec2.images.filter(Filters=filters).all())
latest_image = sorted(images, key=lambda x: x.creation_date, reverse=True)[0]
ami_id = latest_image.id
print(f"The latest Amazon Linux 2 AMI ID is: {ami_id}")

"""
    Here's how it works:
    1. images is a list of Image objects returned by the filter() method,
    which filters the available AMIs based on the specified criteria.
    2. The sorted() function sorts the images list based on the creation_date attribute of each Image object.
    The key argument specifies a function that takes an element of the images list as input and returns a value to use as the sort key.
    In this case, the lambda function lambda x: x.creation_date takes an Image object as input (x)
    and returns its creation_date attribute, which is used as the sort key.
    3. The reverse=True argument specifies that the list should be sorted in descending order (i.e., from newest to oldest AMI).  
    4. Finally, [0] selects the first item (i.e., the most recent AMI) in the sorted list and assigns it to the latest_image variable.
    So, latest_image will contain the Image object representing the most recent Amazon Linux AMI that matches the specified filter criteria.
"""