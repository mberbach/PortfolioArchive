# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 12:09:08 2023

@author: mberbach

tree = lxml.parse.(url)
urlList[] = tree.xpath(xpath)
for x in urlList
  fname = string.method.tail(urlList)
  urllib.request.urlretrive(x, fname)
"""
import lxml.html
import urllib.request as req
import ssl

# disable SSL verification for HTTPS requests
ssl._create_default_https_context = ssl._create_unverified_context
url = "https://www.irs.gov/charities-non-profits/form-990-series-downloads"
# open the URL and get the HTTP response
res = req.urlopen(url)
# parse the HTML content of the response using lxml
tree = lxml.html.parse(res)
# XPath expression to select all links containing '.zip'
path = "//a[contains(@href,'.zip')]/@href"

# get a list of all matching links in the HTML document
urlList = tree.xpath(path)

# this is for testing xpathing
#print(urlList[1])

# If used to cease download after 2 iterations of loop
# proves it would work were if condition were removed
i = 0
for x in urlList:
  if i < 2:
    fname = x.split('/')[-1]
    print(f"Downloading {x} to current working directory \nRenaming to {fname}\n")
    req.urlretrieve(x, fname)
    tmp = req.urlretrieve(x)
    i += 1
  else:
    print("\nExecuting break to prevent full download.")
    break
