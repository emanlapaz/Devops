import webbrowser
import boto3

def upload_to_bucket():
    # initialize S3 client
    s3 = boto3.client('s3')

    # set the bucket name and image file name
    s3_buck = bucket_name
    wit_logo = 'image.jpg'
    index = 'index.html'

    # upload the image to the bucket and make it public
    s3.upload_file(wit_logo, s3_buck, wit_logo)
    s3.put_object_acl(Bucket=s3_buck, Key=wit_logo , ACL='public-read')
    print("upload 1 done")
    s3.upload_file(index, s3_buck, index)
    s3.put_object_acl(Bucket=s3_buck, Key=index , ACL='public-read')
    print("upload 2 done")

    # open the image in the default web browser
    url = f"http://{bucket_name}.s3-website-{region}.amazonaws.com/{wit_logo}"
    webbrowser.open(url)
