# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 11:13:09 2023

@author: mberbach

In:
    bash handed .zip name

calc:
    open zip
    parse/build xml tree
    search xml- honed
    count non returns? - for xml testin
    
out:
    spits out csv in terms of a table
    nonprofit|revenue|year

notes:
    target orgs in file
solved-moved up for clarity:
    zp is xml file name?
    whats the diff between zf and fname? If zf stores fname? is fname a direct xml reference?
        I was confusing objects/names/files
        
CSV writer as part of function scrapped- writing to same file in parallel will be hard to sort out
"""
# at this point I think Ill have to start parsing full years to properly look for the
# non-profit I need, might be worth building the pipe now. Need the syntax that will handle 
# all files for a year.
# worth building out into parallel at this point to speed up process

import zipfile
from lxml import etree
import sys

# works when I hardcode directory
# print(zipfile.is_zipfile(sys.stdin))
# print(sys.stdout)

# read zip file path from standard input
zpath = sys.argv[1]
zp = zipfile.ZipFile(zpath)
fnames = zp.namelist()
mt = 0

def xtract(fname, zp, mt):    
    f = zp.open(fname)
    tree = etree.parse(f)
    # reducers
    ns = {'irs':'http://www.irs.gov/efile'}
    xnam = '//irs:Filer/irs:BusinessName/irs:BusinessNameLine1Txt/text()'
    #xein = '//irs:Filer/irs:EIN/text()'
    #xdsc = '//irs:DescriptionProgramSrvcAccomTxt/text()'
    xweb = '//irs:IRS990EZ/irs:WebsiteAddressTxt/text()'
    # happy tails tax ID is 68-0317260
    # using xpath to extract same text
    # find path in xml, place after irs:
    snam = str(tree.xpath(xnam, namespaces = ns))
    #sein = str(tree.xpath(xein, namespaces = ns))
    #sdsc = str(tree.xpath(xdsc, namespaces = ns))
    sweb = str(tree.xpath(xweb, namespaces = ns))
    keyFi = "HAPPY TAILS ANIMAL SANCTUARY"

    if len(snam) != 0 and keyFi == snam:
        
        print('File: '+fname)
        print(snam)
        print('Website:' sweb)
        print('\n')
    else:
        mt += 1
    
    
    return mt
    
#gogoRite - csv in python faster than reading out
def gogo(mt):
    #n = 3
    #i = 0
    #for line in sys.stdin:
    for x in fnames:
        #if i < n:
        mt = xtract(x,zp,mt)
          # i += 1 
    print(mt)
gogo(mt)

