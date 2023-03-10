<img src="https://github.com/emanlapaz/Devops/blob/master/images/devops.jpg" width=100% height=100%>

This code is a Python script that uses the Boto3 library to create an Amazon Elastic Compute Cloud (EC2) instance and an Amazon Simple Storage Service (S3) bucket in the user's Amazon Web Services (AWS) account. It also downloads an image from a URL, uploads it to the created S3 bucket, and opens the image in the user's default web browser.

The script starts by importing necessary libraries such as boto3, webbrowser, time, sys, random, string, and urllib.request. It then creates an EC2 instance by getting the latest Amazon Machine Image (AMI) ID and creating a new instance using the specified AMI ID, instance type, and security group. The script also installs Apache HTTP server and starts it on the EC2 instance using the UserData parameter.

After the EC2 instance is created, the script gets the public IP address of the instance and opens the web browser to display the Apache HTTP server default page. The script then creates an S3 bucket by randomly generating a unique name, uploads an image to the bucket, and sets the object ACL to public-read. It also creates an index.html file and sets the website configuration for the bucket to use the index.html file as the default document and error.html file as the error document.

Overall, this script demonstrates how to use the Boto3 library to create and manage AWS resources such as EC2 instances and S3 buckets.


References:
    Boto3 EC2 Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html - This is the official Boto3 documentation for the EC2 service. It provides detailed information on how to use the service and its methods.

    EC2 Image Filters: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/finding-an-ami.html - This AWS documentation provides more information on EC2 Image Filters and how they can be used to search for Amazon Machine Images (AMIs).

    Python's lambda functions: https://docs.python.org/3/reference/expressions.html#lambda - This is Python's documentation on lambda functions, which are anonymous functions that can be used as arguments to higher-order functions.

    Sorting lists in Python: https://docs.python.org/3/howto/sorting.html - This page explains how to sort lists in Python, which is used in the code to sort a list of EC2 images by their creation date.

    The EC2 Image class in Boto3: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#image - This is the official documentation for the Image class in Boto3, which is used to represent EC2 images. It provides information on the attributes and methods of the class.
