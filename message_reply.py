# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 10:57:42 2018

@author: Raghav Utpat
"""

import pandas as pd
import praw
from praw.models import Message

reddit=praw.Reddit('bot1')
inbox=reddit.inbox

def reply(author,c_id):
    infile='D:/Bot/deletedcomments.csv'
    df=pd.read_csv(infile)
    c_body=df.loc[df['comment_id']==c_id,'comment_text'].iloc[0]
    plink=df.loc[df['comment_id']==c_id,'permalink'].iloc[0]
    text='I undeleted [this comment]('+plink+') for you. Here it is:    \n"'+c_body+'"    \nFor more info visit [r/_undelete_Bot](https://www.reddit.com/r/_undelete_Bot/)'
    author.message('Hello , _undelete_Bot here',text)

def main():    
    for item in reddit.inbox.unread(limit=None):
        if isinstance(item, Message):
            print(item.body)
            print(item.subject)
            print(item.author)
            if(item.subject=='Undelete'):
                reply(item.author,item.body)
                item.mark_read()
                

if __name__=="__main__":
    main()