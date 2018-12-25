# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 19:11:05 2018

@author: Raghav Utpat
"""

import os
from datetime import datetime
import praw
import pandas as pd


columns=['comment_id','comment_text','dvotes','uvotes','created_utc','controversiality','author','permalink','submission','score_hidden']
c_id=[]
c_text=[]
uvotes=[]
deleted=[]          #holds ids of deleted comments
date=[]
link=[]
controversiality=[]
author=[]
in_submission=[]
score_hidden=[]
votes_now=[]
submission_list=[]

reddit=praw.Reddit('bot1')


def crawl(subr,LIMIT,VERBOSE,mode):
    
    subreddit=reddit.subreddit(subr)
    newcomments=0
    newdeletes=0
    deletedcomments=0   #comments that have been deleted before their text was recorded
    num_submissions=0
    outfile='D:/Bot/'+subr.capitalize()+'/'+subr+'out.csv'
    deletedfile='D:/Bot/'+subr.capitalize()+'/'+subr+'deleted.csv'
    
    
    if not os.path.isfile(outfile):
        for submission in getattr(subreddit,mode.swapcase())(limit=LIMIT):     #calls function acc. to string
            num_submissions+=1
            print('No. of submissions crawled = %r'%(num_submissions))
            if not submission_list:
                submission_list.append(submission.id)
            elif submission.id not in submission_list:   #check if submission was crawled in another sorting mode
                submission_list.append(submission.id)
            else:                                        #if yes skip it
                continue
            if(VERBOSE):
                print("Crawling submission: \n%s"%(submission.title))
            submission.comments.replace_more()
            for comment in submission.comments.list():
                if(comment.body=='[deleted]'):
                    deletedcomments+=1
                else:
                    newcomments+=1
                    c_id.append(comment.id)
                    c_text.append(comment.body)
                    uvotes.append(comment.ups)
                    date.append(comment.created_utc)
                    controversiality.append(comment.controversiality)
                    author.append(comment.author)
                    link.append(comment.permalink)
                    in_submission.append(comment.submission)
                    score_hidden.append(comment.score_hidden)
    else:
        df1=pd.read_csv(outfile)
        for submission in getattr(subreddit,mode.swapcase())(limit=LIMIT):
            num_submissions+=1
            print('No. of submissions crawled = %r'%(num_submissions))
            if not submission_list:
                submission_list.append(submission.id)
            elif submission.id not in submission_list:   #check if submission was crawled in another sorting mode
                submission_list.append(submission.id)
            else:
                continue
            if(VERBOSE):
                print("Crawling submission: \n%s"%(submission.title))
            submission.comments.replace_more()
            for comment in submission.comments.list():
                if(comment.id in df1[columns[0]].values):
                    if(comment.body=='[deleted]'):
                        print("Found a deleted comment in our db")
                        if not os.path.isfile(deletedfile):
                            print("Adding it to the file...")
                            newdeletes+=1
                            deleted.append(comment.id)
                            votes_now.append(comment.ups)
                        
                        
                        else:
                            del_df=pd.read_csv(deletedfile)
                            if(comment.id not in del_df['deleted comments'].values):
                                print("Adding it to the file...")
                                newdeletes+=1
                                deleted.append(comment.id)
                                votes_now.append(comment.ups)
                            else:
                                continue
                    else:
                        continue
                else:
                    if(comment.body=='[deleted]'):
                        deletedcomments+=1
                    else:
                        newcomments+=1
                        c_id.append(comment.id)
                        c_text.append(comment.body)
                        uvotes.append(comment.ups)
                        date.append(comment.created_utc)
                        controversiality.append(comment.controversiality)
                        author.append(comment.author)
                        link.append(comment.permalink)
                        in_submission.append(comment.submission)
                        score_hidden.append(comment.score_hidden)
    print("Done crawling :)")
    
    analysis(newcomments,newdeletes,deletedcomments,subr,mode)
    


def analysis(newcomments,newdeletes,deletedcomments,subr,mode):
    
    if not os.path.exists('D:/Bot/'+subr.capitalize()):
        os.makedirs('D:/Bot/'+subr.capitalize())
    logfile='D:/Bot/'+subr.capitalize()+'/'+subr.swapcase()+'LOG.txt'
    
    print("\nAnalysis :\nMode = %r\nNew Comments = %r\nNew Deletions = %r\nDeleted Comments Encountered = %r"%(mode,newcomments,newdeletes,deletedcomments))
    print("Writing to log...")
    
    with open(logfile, mode='a') as file:
        file.write('%s====================\nAnalysis :\nMode = %r\nNew Comments = %r\nNew Deletions = %r\nDeleted Comments Encountered = %r\n=================' % 
               (datetime.now(),mode,newcomments,newdeletes,deletedcomments))
        
        

def write_df(subr):
    
    outfile='D:/Bot/'+subr.capitalize()+'/'+subr+'out.csv'
    deletedfile='D:/Bot/'+subr.capitalize()+'/'+subr+'deleted.csv'
    
    date1=[(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')) for x in date]
    data={columns[0]:c_id,columns[1]:c_text,columns[3]:uvotes,columns[4]:date1,columns[5]:controversiality,columns[6]:author,columns[7]:link,columns[8]:in_submission,columns[9]:score_hidden}
    df=pd.DataFrame.from_dict(data)


    if not os.path.isfile(outfile):
        df.to_csv(outfile,index=False)
    else:                                       #if file is present append to it without column names
        df.to_csv(outfile,mode='a',index=False,header=False)


    if deleted:
        deleted_dict={'deleted comments':deleted,'votes now':votes_now}
        df2=pd.DataFrame.from_dict(deleted_dict)
        if not os.path.isfile(deletedfile):
            df2.to_csv(deletedfile,index=False)
        else:                                   #if file is present append to it without column names
            df2.to_csv(deletedfile,mode='a',index=False,header=False)



def main():
    subs=['worldnews','news','todayilearned','politics','europe','tumblr']
    LIMIT=30
    VERBOSE=True
    modes=['HOT','RISING']
    for subr in subs:
        if(VERBOSE):
            print("\nCrawling %s\n"%(subr))
        for mode in modes:
            if(VERBOSE):
                print("\nSorting by %s\n"%(mode))
            '''Empty all lists before function call'''
            del c_id[:]
            del c_text[:]
            del uvotes[:]
            del deleted[:]
            del date[:]
            del link[:]
            del controversiality[:]
            del author[:]
            del in_submission[:]
            del score_hidden[:]
            del votes_now[:]
            crawl(subr,LIMIT,VERBOSE,mode)
            write_df(subr)
        del submission_list[:]    #empties the list
        
if __name__ == "__main__":
    main()