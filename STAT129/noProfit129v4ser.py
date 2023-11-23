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
#mt = 0
ns = {'irs':'http://www.irs.gov/efile'}


def anvil(tree):
    misDsc = str(tree.xpath('//irs:ReturnData/irs:IRS990/irs:MissionDesc/text()', namespaces = ns))
    actMisDsc = str(tree.xpath('//irs:ReturnData/irs:IRS990/irs:ActivityOrMissionDesc/text()', namespaces = ns))
    dsc = str(tree.xpath('//irs:ReturnData/irs:IRS990/irs:Desc/text()', namespaces = ns))
    lst = [misDsc,actMisDsc,dsc]
    #print(lst)
    patUn = re.compile(r'native plant|biodiversity|wildlife', flags=re.IGNORECASE)
    #patDi = re.compile(r'native plant|natural habitat',flags=re.IGNORECASE)
    swch = 0
    #patTri = re.compile(,re.IGNORECASE)
    
    for txt in lst:
        matchUn = re.search(patUn,txt)
        #matchDi = re.search(patDi,txt)
        if matchUn != None and swch == 0:
        
            swch = 1
            snam = etch(tree)
            matchUn = re.search(r"\d{4}",zstr)
            yrstr = matchUn.group()
            cyrev = str(tree.xpath('//irs:ReturnData/irs:IRS990/irs:CYTotalRevenueAmt/text()', namespaces = ns))
            cyrev = cyrev[2:-2]
            if len(snam) > 2:
                print(snam+','+ cyrev +','+yrstr)


def etch(tree):
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


def xtract(fname):    
    f = zp.open(fname)
    tree = etree.parse(f)

    anvil(tree)
    

def gogo():
    for x in fnames:
        xtract(x) 
    print()
gogo()