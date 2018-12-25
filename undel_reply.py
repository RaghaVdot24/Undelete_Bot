# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 16:13:46 2018

@author: Raghav Utpat
"""

import os
import time
import praw
import pandas as pd

reddit=praw.Reddit('bot1')

ret_id=[]
text1="[Click here and I'll PM you the comment](https://www.reddit.com/message/compose/?to=_undelete_Bot&subject=Undelete&message="
text2=")    \n^(I'm a bot bleep-boop. I'm in beta, please don't hurt me. PM any problems [to this guy](https://reddit.com/user/crawlerx3001) or [this guy](https://reddit.com/user/VdotOne))    \n^(You can summon me by replying with \"!undelete\" to the top child of a deleted comment(on select subs only)^)    \n^(Please visit r/undelete_Bot for more info)"


def undelete_reply(subr):
    infile='D:/Bot/'+subr.capitalize()+'/'+subr+'deletedcopy.csv'
    infile2='D:/Bot/'+subr.capitalize()+'/'+subr+'deleted.csv'
    outfile='D:/Bot/'+subr.capitalize()+'/'+subr+'botcomments.csv'
    replied_to=[]
    
    df1=pd.read_csv(infile)
    df1.drop_duplicates(subset='comment_id',inplace=True)
    for r_id in df1['comment_id']:
        deleted_comm=reddit.comment(r_id)
        deleted_comm.refresh()
        child_comment=deleted_comm.replies[0]
        (returned_id,flag)=reply_to_child(child_comment,r_id)
        if(flag==False):
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


def reply_to_child(child_comment,r_id):
    for child_reply in child_comment.replies:
        if(child_reply.body=="!undelete" or child_reply.body=="!Undelete"):
            try:
                returned_id=child_reply.reply(text1+r_id+text2)
                return(True,returned_id)
            except praw.exceptions.APIException as e:
                print(e.message)
                return(False,0)
    return(False,0)

def main():
    subs=['tumblr']
    for sub in subs:
        print('Running sub %s' %(sub))
        undelete_reply(sub)
        
if __name__=="__main__":
    main()