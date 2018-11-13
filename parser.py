#!/usr/bin/env python

"""
USAGE:

$ parser.py log_file
"""

import os
import re
import sys
import csv

myregex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

def log_reader(logfile):
    cnt = 0
    with open(logfile) as f:
        for line in f:
            ips = re.findall(myregex, line)
            print("{}: {} == {}".format(cnt, line.strip(), ips))
            cnt += 1

def main():
    if not len(sys.argv) > 1:
        print (__doc__)
        sys.exit(1)
    log_file = sys.argv[1]
    log_reader(log_file)


if __name__ == '__main__':
    main()
