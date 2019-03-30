 
#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import json
import os
import subprocess
import multiprocessing
import sys
 
 
POOL_SIZE = 4  # number of parallel downloads
 
 
def download(item):
    local, remote = item
    subprocess.check_call([ 'gsutil', 'cp', remote, local])
 
 
def main():
    will_download = {}
    args = sys.argv[1:]
    if len(args) < 1:
        input_file = sys.stdin
    elif len(args) == 1:
        input_file = open(args[0])
    else:
        exit('Usage: download.py [json_file]')
 
    for line in input_file:
        d = json.loads(line)
        remote, local = d['remote'], d['local']
 
        if os.path.exists(local):
            continue

        will_download[local] = remote
 
    pool = multiprocessing.Pool(POOL_SIZE)
    pool.map(download, will_download.iteritems())
 
 
 
if __name__ == '__main__':
    main()
