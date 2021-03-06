# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 20:34:39 2018

@author: Raghav Utpat
"""

import os
import pandas as pd


def arrange(subr,dfx):
    infile1='D:/Bot/'+subr.capitalize()+'/'+subr+'out.csv'
    infile2='D:/Bot/'+subr.capitalize()+'/'+subr+'deleted.csv'
    outfile='D:/Bot/'+subr.capitalize()+'/'+subr+'deletedcopy.csv'
    outfile2='D:/Bot/'+subr.capitalize()+'/'+subr+'deletedrefer.csv'
        
    df1=pd.read_csv(infile1)
    if not os.path.isfile(infile2):
        return
    df2=pd.read_csv(infile2)
        
    delx=list(df2['deleted comments'])
        
    df4=df1[df1['comment_id'].isin(delx)]
    print(df4.info())
    df4.drop_duplicates(subset='comment_id',inplace=True)
    #print(df4.info())
    
    df4.to_csv(outfile,index=False)
    df4.to_csv(outfile2,index=False)
    
    dfx=pd.concat([dfx,df4],ignore_index=True)
    return dfx

def main():
    groupedfile='D:/Bot/deletedcomments.csv'
    df=pd.DataFrame()
    if os.path.isfile(groupedfile):
        df=pd.read_csv(groupedfile)
    subs=['todayilearned','politics','europe','tumblr']
    for sub in subs:
        df=arrange(sub,df)
    print(df.info())
    df.drop_duplicates(subset='comment_id',inplace=True)
    df.to_csv(groupedfile,index=False)
        
        
if __name__=="__main__":
    main()