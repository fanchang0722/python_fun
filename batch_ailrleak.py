# -*- coding: utf-8 -*-
"""
Script to batch process all airleak test log
Created on 10/19/2017

@author: fanchang
"""
import sys
import os
import re

# folder = r'/Users/fanchang/Downloads/Air Leak Full Device'
# outputFile = r'ouput.csv'

def airleakAnalysis(folder, outputFile):
    fout = open(outputFile, 'w')
    for filename in os.listdir(folder):
        if filename.endswith('txt'):
        # print filename
            tempname = filename.split('_')
        # print tempname[2][:9], tempname[3]
            fp = open(os.path.join(folder, filename), 'r')
            strings = fp.read()
            output = re.findall(r'[^\r\n.]+', strings)
            if len(output) > 2:
                MSB = output[1].split(' ')
                LSB = output[2].split(' ')
                print tempname[2][:9], tempname[3:5], MSB[-1]+'.'+LSB[0]
                stringOut=str(tempname[2][:9])+','+str(tempname[3:5])+','+str(MSB[-1])+'.'+str(LSB[0])+'\r\n'
                fout.writelines(stringOut)
            else:
                print tempname[2][:9], tempname[3:5], 'Server leak'
                stringOut=str(tempname[2][:9])+','+str(tempname[3:5])+',Server leak'+'\r\n'
                fout.writelines(stringOut)
    fout.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "you did NOT give any arguments\n"
    else:
        print sys.argv[1:3]
        folder = sys.argv[1]
        outputFile = sys.argv[2]
        airleakAnalysis(folder, outputFile)
