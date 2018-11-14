#!/usr/bin/env python

"""
USAGE:

$ parser.py log_file
"""

import os
import re
import sys
import csv
import pandas as pd
from urllib.parse import urlparse, parse_qs

functions = [
    'getAdv',
    'getVideoData',
    'getVideoDataSearch',
]

# APIRegex -> Eg. getAdv?zone=news_diretta&cliente=0&_=1540695247997
APIRegex = r'.* - - \[\d+\/\w+/\d+:\d+:\d+:\d+ \+\d+\] "GET \/be\/([^\?]+\?[^ ]*)'
# FunctionRegex -> Eg. getAdv
FunctionRegex = r'([^\?]*)'
# ParametersRegex -> Eg. zone=news_diretta&cliente=0&_=1540695247997
ParametersRegex = r'\?([^ ]*)'

def open_file(file_path):
    f = open(file_path, "w")
    f.write('function,parameters\n')
    return f

def write_entry(f, function, parameters):
    if parameters:
        f.write(function+","+parameters+"\n")

def close_file(f):
    f.close()

def log_reader(logfile, outputFiles):
    global functions
    with open(logfile) as f:
        print("function,parameters")
        for line in f:
            # I found a GET API call
            match1 = re.findall(APIRegex, line)
            if match1:
                parsed_url = urlparse(match1[0])
                queryString = parse_qs(parsed_url.query)
                # Check if token is not a queryString parameter
                if "token" not in queryString:
                    match2 = re.findall(FunctionRegex, match1[0])
                    if match2 and match2[0] in functions:
                        match3 = re.findall(ParametersRegex, match1[0])
                        print("{},{}".format(match2[0], match3[0]))
                        write_entry(outputFiles[match2[0]], match2[0], match3[0])


def main():
    if not len(sys.argv) > 1:
        print (__doc__)
        sys.exit(1)
    global functions
    outputFiles = {}
    log_file = sys.argv[1]
    for f in functions:
        outputFiles[f] = open_file(log_file+"."+f+".csv")
    log_reader(log_file, outputFiles)
    for f in outputFiles:
        close_file(outputFiles[f])

if __name__ == '__main__':
    main()
