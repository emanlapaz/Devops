#!/usr/bin/env python3
import urllib.request

#url to download image
url = "http://devops.witdemo.net/logo.jpg"
#output path to images folder
output_path = "/home/eugene/Devops/images/image.jpg"

urllib.request.urlretrieve(url, output_path)