# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 15:39:09 2018

@author: Raghav Utpat
"""

import os.path
import pandas as pd


def del_duplicates(subr):
    infile1='D:/Bot/'+subr.capitalize()+'/'+subr+'out.csv'
    infile2='D:/Bot/'+subr.capitalize()+'/'+subr+'deleted.csv'
    infile3='D:/Bot/'+subr.capitalize()+'/'+subr+'deletedcopy.csv'
    infile4='D:/Bot/'+subr.capitalize()+'/'+subr+'deletedrefer.csv'
    infile5='D:/Bot/'+subr.capitalize()+'/'+subr+'discarded.csv'
    
    for file in [infile1,infile2,infile3,infile4,infile5]:
        if not os.path.isfile(file):
            continue
        df1=pd.read_csv(file)
        count1=len(df1.iloc[:,[0]])
        df1.drop_duplicates(inplace=True)
        count2=len(df1.iloc[:,[0]])
        print(file)
        print('%r - %r = %r'%(count1,count2,count1-count2))
        #df1.to_csv(file,index=False)

def main():
    subs=['worldnews','news','todayilearned','politics','europe','tumblr']
    for sub in subs:
        del_duplicates(sub)
        
        
if __name__=="__main__":
    main()