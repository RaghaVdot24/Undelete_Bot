# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 06:39:03 2018

@author: Raghav Utpat
"""

import os
import time
import praw
import pandas as pd

reddit=praw.Reddit('bot1')

ret_id=[]
text1="Hey anyone wants to see what was in the parent comment ?    \nAnyone wants to know the secret stuff ?    \n[Click here and I'll PM you](https://www.reddit.com/message/compose/?to=_undelete_Bot&subject=Undelete&message="
text2=")    \n^(I'm a bot bleep-boop. I'm in beta, please don't hurt me. PM any problems [to this guy](https://reddit.com/user/crawlerx3001^) or [this guy](https://reddit.com/user/VdotOne))    \n^(You can summon me by replying !undelete to a deleted comment(on select subs only)^)    \n^(Please visit r/undelete_Bot for more info)"



def reply(subr,num_comments):
#TODO handle case where deletedcopy is not present
    infile='D:/Bot/'+subr.capitalize()+'/'+subr+'deletedcopy.csv'
    infile2='D:/Bot/'+subr.capitalize()+'/'+subr+'deleted.csv'
    outfile='D:/Bot/'+subr.capitalize()+'/'+subr+'botcomments.csv'
    replied_to=[]
    
    if not os.path.isfile(infile):
        df1=pd.read_csv(infile)
    df1.drop_duplicates(subset='comment_id',inplace=True)
    n=len(df1.index)
    print(n)
    x=min(num_comments,n)
    random_rows=df1.sample(x)['comment_id']
    for r_id in random_rows:
        comm=reddit.comment(r_id)
        comm.refresh()
        child_comment=comm.replies[0]
        print(child_comment)
        try:
            returned_id=child_comment.reply(text1+r_id+text2)
        except praw.exceptions.APIException as e:
            print(e.message)
            continue
        time.sleep(180)
        replied_to.append(r_id)
        ret_id.append(returned_id)
        
    '''Drop rows from deletedcopy.csv using comment ids replied to and write it to file'''
    df1=df1[~df1['comment_id'].isin(replied_to)]
    df1.to_csv(infile,index=False)
    
    
    '''Drop rows from deleted.csv using comment ids replied to write it to file'''
    df_deleted=pd.read_csv(infile2)
    df_deleted=df_deleted[~df_deleted['deleted comments'].isin(replied_to)]
    print(df_deleted.info())
    df_deleted.to_csv(infile2,index=False)
    

    ret_dict={'comment_id':ret_id}
    df3=pd.DataFrame.from_dict(ret_dict)
    
    if not os.path.isfile(outfile):
        df3.to_csv(outfile,index=False)
    else:
        df3.to_csv(outfile,mode='a',index=False,header=False)


def main():
    #subs=['worldnews','news','todayilearned','politics','europe','tumblr']
    subs=['todayilearned','politics','europe','tumblr']
    num_comm=1
    for sub in subs:
        print('Running sub %s' %(sub))
        reply(sub,num_comm)
        
if __name__=="__main__":
    main()