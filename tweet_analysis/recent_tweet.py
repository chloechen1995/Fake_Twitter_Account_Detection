#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 14:37:58 2017

@author: Chloechen
"""


"""
The follwoing codes select the most recent 200 tweets 
"""

#%%
import os
import pandas as pd
import glob

#%%

sample = "/Users/Chloechen/Desktop/Sample"
for csvfile in sample:
    os.chdir(sample)
    base = '/Users/Chloechen/Desktop/Sample_Tweets'
    files = glob.glob('*.csv')
    
    for file_name in files:
        os.chdir(sample)
        try:
            df_200 = pd.read_csv(file_name, nrows = 200)
        except pd.parser.CParserError:
            df_200 = pd.read_csv(file_name)
        os.chdir(base)
        df_200.to_csv(file_name) 
