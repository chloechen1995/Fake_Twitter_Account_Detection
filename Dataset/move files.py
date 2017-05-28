import os
import pandas as pd
os.chdir('/Users/Aaron/Desktop/Data')
import glob
#%%
path_list = ['/Users/Aaron/Desktop/Data/Tweet_' + str(i) for i in range(20)]
colnames = ['Tweet_Id', 'Created_At', 'Source', 'Favorite_Count', 'Retweet_Count', 'Tweet_Text', 'User_Id']
colnames_n = ['Index','Tweet_Id', 'Created_At', 'Source', 'Favorite_Count', 'Retweet_Count', 'Tweet_Text', 'User_Id']

for path in path_list:
    os.chdir(path)
    base = '/Users/Aaron/Desktop/Sample'
    files = glob.glob('*.csv')
    
  
    for file_name in files:
        os.chdir(path)
        #print file_name
        try:
            df = pd.read_csv(file_name)
            df.columns = colnames_n
            df.drop('Index', 1)
        except ValueError:
            df.columns = colnames
        os.chdir(base)
        df.to_csv(file_name)  