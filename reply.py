# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 06:39:03 2018

@author: Raghav Utpat
"""

import os
import praw
import pandas as pd

reddit=praw.Reddit('bot1')

replied_to=[]
ret_id=[]
text1="Hey anyone wants to see what was in the parent comment ?    \nAnyone wants to know the secret stuff ?    \n[Click here and I'll PM you](https://www.reddit.com/message/compose/?to=_undelete_Bot&subject=Undelete&message="
text2=")    \n^(I'm a bot bleep-boop. I'm in beta, please don't hurt me. PM any problems [to this guy](https://reddit.com/user/crawlerx3001) or [this guy](https://reddit.com/user/VdotOne))    \n^(You can summon me by replying !undelete to a deleted comment(on select subs only)^)"



def reply(subr,num_comments):
#TODO handle case where deletedcopy is not present
    infile='D:/Bot/'+subr.capitalize()+'/'+subr+'deletedcopy.csv'
    outfile='D:/Bot/'+subr.capitalize()+'/'+subr+'botcomments.csv'
    
    df1=pd.read_csv(infile)
    df1.drop_duplicates(subset='comment_id',inplace=True)
    n=df1.count()
    random_rows=df1.sample(min(num_comments,n))['comment_id']
    l=list(random_rows.index.values)
    replied_to.append(l)
    for r_id in random_rows:
        comm=reddit.comment(r_id)
        child_comment=give_child(r_id)
        print(child_comment)
        returned_id=child_comment.reply(text1+r_id+text2)
        ret_id.append(returned_id)
        
    df1=df1.drop(replied_to)
    ret_dict={'comment_id':ret_id}
    df3=pd.DataFrame.from_dict(ret_dict)
    
    df1.to_csv(infile,index=False)
    if not os.path.isfile(outfile):
        df3.to_csv(outfile,index=False)
    else:
        df3.to_csv(outfile,mode='a',index=False,header=False)


def give_child(c_id):
    submission=reddit.comment(c_id).submission
    submission.comments.replace_more()
    for c in submission.comments.list():
        if(c.parent().id==c_id):
            return c


def main():
    subs=['worldnews','news','todayilearned','politics','europe','tumblr']
    #subs=['pythonforengineers']
    num_comm=5
    for sub in subs:
        print('Running sub %s' %(sub))
        reply(sub,num_comm)
        
if __name__=="__main__":
    main()