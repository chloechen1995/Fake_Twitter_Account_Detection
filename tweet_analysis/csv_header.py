#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 14:05:43 2017

@author: Chloechen
"""

#%%

## Reference: https://stackoverflow.com/questions/16306819/python-edit-csv-headers

"""
The codes below change the headers of the csv files so that the tweets.csv have consistent headers
"""
import csv
import os
import glob

sample_selection = '/Users/Chloechen/Desktop/Sample_Tweets'

os.chdir(sample_selection)
files = glob.glob('*.csv')

for file_name in files:
    inputFileName = file_name
    outputFileName = os.path.splitext(inputFileName)[0] + "_.csv"

    with open(inputFileName, 'rb') as inFile, open(outputFileName, 'wb') as outfile:
	    r = csv.reader(inFile)
	    w = csv.writer(outfile)

	    next(r, None)  # skip the first row from the reader, the old header
	    # write new header
	    w.writerow(['Index_1', 'Index_2', 'Tweet_ID', 'Created_At', 'Source', 'Favorite_Count', 'Retweet_Recount', 'Tweet_Text', 'User_ID' ])

	    for row in r:
	       w.writerow(row)