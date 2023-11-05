# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 12:13:03 2023

@author: Niko
"""
import re
import sys
import zipfile
from lxml import etree

datafile = sys.argv[1]

#z5 = zipfile.ZipFile("first-5-tax-returns.zip")
z = zipfile.ZipFile(datafile)

ns = {'irs':'http://www.irs.gov/efile'}

#text = "Animal shelter"

# Write our function
def extract(fname, zfile, text = "Students"):
    """
    Extract important tax return data from each .xml file
    for analysis
    
    
    fname: the name of a file inside the .zip
    zfile: an open .zip archive downloaded from IRS 990
    
    """
    f = zfile.open(fname)
    tree = etree.parse(f)

    ns = {'irs':'http://www.irs.gov/efile'}
    result = {}
    result["Name"] = tree.xpath('//irs:Filer/irs:BusinessName/irs:BusinessNameLine1Txt/text()',
                                namespaces = ns)[0]
    
    # using xpath to extract same text
    Mission = tree.xpath('//irs:DescriptionProgramSrvcAccomTxt/text()',
                                   namespaces = ns)
    if len(Mission) == 0:
        return None
    
    p = re.compile(text, re.IGNORECASE)
    
    if p.search(Mission[0]):
        pass
    else:
        return None
    
    
    r = tree.xpath('//irs:TotalRevenueAmt/text()', 
                                        namespaces = ns)[0]
    result["TotalRevenue"] = float(r)
    
    
    e = tree.xpath('//irs:TotalExpensesAmt/text()',
                                         namespaces = ns)[0]
    result["TotalExpenses"] = float(e)
    
    y = tree.xpath('//irs:TaxYr/text()', namespaces = ns)[0]
    
    result["Year"] = int(y)
    
    return result

#p = re.compile(text, re.IGNORECASE)
#p.search("Animals are cool")


# call this function
# extract('202000069349200000_public.xml', z)

# Apply the function to all the data
print([extract(fn, z) for fn in z.namelist()])
#print(summaries)

# let's pull all the names out
#a = [x["Name"] for x in summaries]
#print(a)