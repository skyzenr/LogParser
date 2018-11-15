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

extension = ".csv"

functions = [
    'getAdv',
    'getVideoData',
    'getVideoDataSearch',
    'getVODAccessToken.do',
    'getVideoLogo',
    'getPlaylistVideoData',
    'getPlaylistInfo',
]

# APIRegex -> Eg. getAdv?zone=news_diretta&cliente=0&_=1540695247997
APIRegex = r'.* - - \[\d+\/\w+/\d+:\d+:\d+:\d+ \+\d+\] "GET (?:\/be\/|\/SkyItVideoportalUtility\/)([^\?]+\?[^ ]*) '
# FunctionRegex -> Eg. getAdv
FunctionRegex = r'([^\?]*)'
# ParametersRegex -> Eg. zone=news_diretta&cliente=0&_=1540695247997
ParametersRegex = r'\?([^ ]*)'

def open_file(file_path):
    with open(file_path, "w") as f:
        f.write('function,parameters\n')
    return file_path

def write_entry(file_path, function, parameters):
    if parameters:
        with open(file_path, "a") as f:
            f.write(function+","+parameters+"\n")

def log_reader(logfile, outputFiles):
    global functions
    with open(logfile) as f:
        for line in f:
            # I found a GET API call
            match1 = re.findall(APIRegex, line)
            if match1 and match1[0]:
                api_call = match1[0]
                parsed_url = urlparse(api_call)
                queryString = parse_qs(parsed_url.query)
                match2 = re.findall(FunctionRegex, api_call)
                match3 = re.findall(ParametersRegex, api_call)
                if match2 and match2[0]:
                    if match3 and match3[0]:
                        # Write in global
                        write_entry(outputFiles["global"], match2[0], match3[0])
                        if "token" not in queryString:
                            write_entry(outputFiles["global.notoken"], match2[0], match3[0])
                        # Each function
                        if match2[0] in functions:
                            write_entry(outputFiles["global.functions"], match2[0], match3[0])
                            write_entry(outputFiles[match2[0]], match2[0], match3[0])
                            if "token" not in queryString:
                                write_entry(outputFiles["global.notoken.functions"], match2[0], match3[0])
                                write_entry(outputFiles[match2[0]+".notoken"], match2[0], match3[0])

def main():
    if not len(sys.argv) > 1:
        print (__doc__)
        sys.exit(1)
    global extension
    global functions
    outputFiles = {}
    log_file = sys.argv[1]
    # Each function has its own file
    for function in functions:
        outputFiles[function] = open_file(log_file+"."+function+extension)
        outputFiles[function+".notoken"] = open_file(log_file+"."+function+".notoken"+extension)
    # A global file with all API calls
    outputFiles["global"] = open_file(log_file+"."+"global"+extension)
    # A global file with all API calls (without token as parameter)
    outputFiles["global.notoken"] = open_file(log_file+"."+"global.notoken"+extension)
    # A global file with all API calls belonging to functions
    outputFiles["global.functions"] = open_file(log_file+"."+"global.functions"+extension)
    # A global file with all API calls belonging to functions (without token as parameter)
    outputFiles["global.notoken.functions"] = open_file(log_file+"."+"global.notoken.functions"+extension)
    log_reader(log_file, outputFiles)

if __name__ == '__main__':
    main()
