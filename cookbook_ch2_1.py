#!/anaconda/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 10:15:35 2017

@author: fanchang
"""

import re
line = 'asdf fjdk; afed, fjek,asdf, foo'
print line
newline = re.split(r'[;,\s]\s*', line)
print newline