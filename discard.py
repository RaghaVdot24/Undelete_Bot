# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 16:44:48 2018

@author: Raghav Utpat
"""

import os
from datetime import datetime,timedelta
import pandas as pd

def delete(subr,DIFF):
    infile='D:/Bot/'+subr.capitalize()+'/'+subr+'out.csv'
    discardedfile='D:/Bot/'+subr.capitalize()+'/'+subr+'discarded.csv'
    today=datetime.utcnow()
    df=pd.read_csv(infile,parse_dates=['created_utc'])
    if(df['created_utc'].dtype==object):
        datemask=(df['created_utc'].str.len()>=8)
        df=df[datemask]
    df['created_utc']=pd.to_datetime(df['created_utc'])
    print(df.info())
    mask=(today-df['created_utc']<=timedelta(hours=DIFF))
    df2=df[~mask]
    print(df2.info())
    df=df[mask]
    print(df.info())
    
    df.to_csv(infile,index=False)
    
    if not os.path.isfile(discardedfile):
        df2.to_csv(discardedfile,index=False)
    else:                                       #if file is present append to it without column names
        df2.to_csv(discardedfile,mode='a',index=False,header=False)
        
        
        
def main():
    subs=['worldnews','news','todayilearned','politics','europe','tumblr']
    DIFF=1.5*24
    for sub in subs:
        print('Running sub %s' %(sub))
        delete(sub,DIFF)
        
if __name__ == "__main__":
    main()