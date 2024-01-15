from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask import current_app as app
from application.models import signup,post,UserPosts,follower,user_comment
from .database import db
import secrets 
app.secret_key = secrets.token_hex()


@app.route("/profile/<user_id>",methods=["GET"])
def profile(user_id):
    sql = signup.query.filter_by(user_id=user_id).first()
    dp = sql.profile_pic
    sql2 = user_comment.query.filter_by(fuser_id=user_id).all()
    com_list = []
    for k in sql2:
        fuser_id = k.user_id
        sql3 = signup.query.filter_by(user_id=fuser_id).first()

        com_list.append([sql3.user_name,k.comment,sql3.profile_pic,k.post_id])

    signpost  = UserPosts.query.filter_by(user_id=user_id).all()
    post_list = []
    sql5 = follower.query.filter_by(user_id=user_id).all()
    sql6 = follower.query.filter_by(fuser_id = user_id).all()
    
    following = 0
    for i in sql5:
        following+= 1
    follower1 = 0
    for i in sql6:
        follower1 += 1


    for p in signpost:
        sql1 = post.query.filter_by(post_id=p.post_id).all()
        
     
        for i in sql1:
            post_list.append([i.title,i.desc,i.time,i.picture,i.post_id,i.likes,i.date])
    Posts = len(post_list)

  
    return render_template("profile.html",user_id=user_id,post_list=post_list,pic=dp,name=sql.user_name,com_list=com_list,follower=follower1,following=following,Posts=Posts)


@app.route("/friend/<user_id>/<fuser_id>",methods=["GET"])
def friend(user_id,fuser_id):
    sql = signup.query.filter_by(user_id=fuser_id).first()
    
    dp = sql.profile_pic
 
    sql2 = user_comment.query.filter_by(fuser_id=fuser_id).all()
    com_list = []
    for k in sql2:
        cuser_id = k.user_id
        sql3 = signup.query.filter_by(user_id=cuser_id).first()

        com_list.append([sql3.user_name,k.comment,sql3.profile_pic,k.post_id])

    signpost  = UserPosts.query.filter_by(user_id=fuser_id).all()
    sql5 = follower.query.filter_by(user_id=fuser_id).all()
    sql6 = follower.query.filter_by(fuser_id = fuser_id).all()
    
    following = 0
    for i in sql5:
        following+= 1
    follower1 = 0
    for i in sql6:
        follower1 += 1
    post_list = []
    for p in signpost:
        sql1 = post.query.filter_by(post_id=p.post_id).all()
        for i in sql1:
            post_list.append([i.title,i.desc,i.time,i.picture,i.post_id,i.likes,i.date])
    Posts = len(post_list)
    sql3 = follower.query.filter_by(user_id=user_id,fuser_id=fuser_id).first()
    if sql3:
        return render_template("friend.html",user_id=user_id,fuser_id=fuser_id,post_list=post_list,pic=dp,name=sql.user_name,com_list=com_list,ch=1,Posts=Posts,follower=follower1,following=following)
    return render_template("friend.html",user_id=user_id,fuser_id=fuser_id,post_list=post_list,pic=dp,name=sql.user_name,com_list=com_list,ch=2,Posts=Posts,follower=follower1,following=following)

@app.route("/follow/<user_id>",methods=["GET"])
def following(user_id):
   
    sql = follower.query.filter_by(user_id=user_id).all()
    
    fol = []
    for p in sql:
        
        fol.append(p.fuser_id)
 
    l = []
    for i in fol:
        sql1 = signup.query.filter_by(user_id=i).all()
        for i in sql1:
            
            l.append((i.user_id,i.user_name,i.profile_pic))
    
    
   
    return render_template("follow.html",user_id=user_id,plist=l)

