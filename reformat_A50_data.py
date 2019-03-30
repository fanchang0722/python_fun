#!/usr/bin/python
import sys

fp = open(sys.argv[1], 'r')
fout = open(sys.argv[2], 'w')
#fp = open(r'A50_DVT_light_summary.csv', 'r')
#fout = open(r'A50.csv', 'w')
fout.write(fp.readline())
fp.close()
fp = open(sys.argv[1], 'r')
count = 0
for lines in fp:
	if count % 2 :
		fout.write(lines)
	count += 1

fp.close()
fout.close()
