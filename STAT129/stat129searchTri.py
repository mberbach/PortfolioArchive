# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 19:05 2023

@author: mberbach

Out format:
    nonprofit|revenue|year
 """

import zipfile
from lxml import etree
import sys
import re

# read zip file path from standard input, now accepting as args from GNU Par.
zstr = sys.argv[1]
zp = zipfile.ZipFile(zstr)
fnames = zp.namelist()
mt = 0

def anvil(tree,ns):
    txt = ''
    
    s1nam = str(tree.xpath('//irs:Filer/irs:BusinessName/irs:BusinessNameLine1Txt/text()', namespaces = ns))
    s1nam = s1nam[2:-2].lower().title()

    s2nam = str(tree.xpath('//irs:Filer/irs:BusinessName/irs:BusinessNameLine2Txt/text()', namespaces = ns))
    s2nam = s2nam[2:-2].lower().title()

    if len(s2nam) != 0:
        txt = s1nam + " " + s2nam
    else:
        txt = s1nam

    return txt.strip()


def xtract(fname, zp, zstr,mt):    
    f = zp.open(fname)
    tree = etree.parse(f)
    
    # reducers
    ns = {'irs':'http://www.irs.gov/efile'}
    snam = anvil(tree,ns)

    
    # Search By BusinessName
    cat = "Happy Tails Pet Sanctuary"
    plant = "California Native Plant Society"
    eff = "Electronic Frontier Foundation Inc"
    civNorCal = "American Civil Liberties Union Foundation Of Northern California Inc"
    civNat =  "American Civil Liberties Union Foundation Inc"

    if len(snam) != 0 and (cat == snam or 
                           plant == snam or 
                           eff == snam or 
                           civNorCal == snam or
                           civNat == snam):
        
        match = re.search(r"\d{4}",zstr)
        yrstr = match.group()

        cyrev = str(tree.xpath('//irs:ReturnData/irs:IRS990/irs:CYTotalRevenueAmt/text()', namespaces = ns))
        cyrev = cyrev[2:-2]

        print(snam+','+ cyrev +','+yrstr)

    else:
        mt += 1
    
    
    return mt
    

def gogo(mt):
    for x in fnames:
        mt = xtract(x,zp,zstr,mt) 
    #print(mt)
gogo(mt)