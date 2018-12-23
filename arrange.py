# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 20:34:39 2018

@author: Raghav Utpat
"""

import os
import pandas as pd


def arrange(subr,df):
    infile1='D:/Bot/'+subr.capitalize()+'/'+subr+'out.csv'
    infile2='D:/Bot/'+subr.capitalize()+'/'+subr+'deleted.csv'
    outfile='D:/Bot/'+subr.capitalize()+'/'+subr+'deletedcopy.csv'
    outfile2='D:/Bot/'+subr.capitalize()+'/'+subr+'deletedrefer.csv'
        
    df1=pd.read_csv(infile1)
    df2=pd.read_csv(infile2)
        
    delx=list(df2['deleted comments'])
        
    df4=df1[df1['comment_id'].isin(delx)]
    print(df4.info())
    #df4.drop_duplicates(subset='comment_id',inplace=True)
    #print(df4.info())
    
    df4.to_csv(outfile,index=False)
    df4.to_csv(outfile2,index=False)
    
    df=pd.concat([df,df4],ignore_index=True)
    return df

def main():
    df=pd.DataFrame()
    groupedfile='D:/Bot/deletedcomments.csv'
    subs=['worldnews','news','todayilearned','politics','europe']#,'tumblr']
    #subs=['pythonforengineers']
    for sub in subs:
        df=arrange(sub,df)
    print(df.info())
    df.to_csv(groupedfile,index=False)
        
        
if __name__=="__main__":
    main()