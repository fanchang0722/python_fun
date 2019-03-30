#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 15:25:45 2017

@author: fanchang
"""

import sys, socket

HOST = '192.168.170.26'               # Symbolic name meaning all available interfaces
PORT = 22              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('ls /tmp/')
data = s.recv(1024)
s.close()
print 'Received', repr(data)