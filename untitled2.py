# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 18:53:57 2016

@author: fanchang
"""

import urllib2
from bs4 import BeautifulSoup

url = "http://www.samhsa.gov/data/NSDUH/2k10State/NSDUHsae2010/NSDUHsaeAppC2010.htm"
soup = BeautifulSoup(urllib2.urlopen(url).read())
soup.findAll('table')[0].tbody.findAll('tr')
for row in soup.findAll('table')[0].tbody.findAll('tr'):
    first_column = row.findAll('th')[0].contents
    third_column = row.findAll('td')[2].contents
    print first_column, third_column

#url = "http://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"
#soup = BeautifulSoup(urllib2.urlopen(url).read())
#for row in soup.findAll('table')[2].findAll('tr'):
    