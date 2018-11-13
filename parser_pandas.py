#!/usr/bin/env python

"""
USAGE:

$ parser_pandas.py log_file
"""

import os
import re
import sys
import pandas as pd 
import numpy as np 

def log_reader(log_file):
    s = pd.Series([1,3,5,np.nan,6,8])
    print(s)

def main():
    if not len(sys.argv) > 1:
        print (__doc__)
        sys.exit(1)
    log_file = sys.argv[1]
    log_reader(log_file)

if __name__ == '__main__':
    main()
