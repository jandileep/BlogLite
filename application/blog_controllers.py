from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask import current_app as app
from application.models import signup, post, UserPosts,user_comment,follower
from .database import db
import secrets 
from base64 import b64encode
import base64
app.secret_key = secrets.token_hex()
app.config['UPLOAD_FOLDER'] = "static\images"
#/friend/{{user_id}}/{{fuser_id}}/{{s[4]}}
@app.route("/mine/<user_id>/<fuser_id>/<post_id>",methods=["POST"])
def comment_mine(user_id,fuser_id,post_id):  
    if request.method == "POST":
        comment = request.form["commenter"]
        sql = user_comment(user_id=user_id,fuser_id=fuser_id,post_id=post_id,comment=comment)
        db.session.add(sql)
        db.session.commit()
        return redirect("/profile/"+str(user_id))
@app.route("/friend/<user_id>/<fuser_id>/<post_id>",methods=["POST"])
def comment_u(user_id,fuser_id,post_id):  
    if request.method == "POST":
        comment = request.form["commenter"]
        sql = user_comment(user_id=user_id,fuser_id=fuser_id,post_id=post_id,comment=comment)
        db.session.add(sql)
        db.session.commit()
        return redirect("/friend/"+str(user_id)+'/'+str(fuser_id))
       
@app.route("/homefriend/<user_id>/<fuser_id>/<post_id>",methods=["POST"])
def home_comment(user_id,fuser_id,post_id):  
    if request.method == "POST":
        comment = request.form["commenter"]
        sql = user_comment(user_id=user_id,fuser_id=fuser_id,post_id=post_id,comment=comment)
        db.session.add(sql)
        db.session.commit()
        return redirect("/home/"+str(user_id))

@app.route("/follow/<user_id>/<fuser_id>")
def follow(user_id,fuser_id):
    sql = follower(user_id=user_id,fuser_id=fuser_id)
    db.session.add(sql)
    db.session.commit()
    return redirect("/friend/"+str(user_id)+'/'+str(fuser_id))


@app.route("/unfollow/<user_id>/<fuser_id>",methods=["GET","DELETE"])
def unfollow(user_id,fuser_id):
    sql = follower.query.filter_by(user_id=user_id,fuser_id=fuser_id).first()
    db.session.delete(sql)
    db.session.commit()
    return redirect("/friend/"+str(user_id)+'/'+str(fuser_id))
@app.route("/funfollow/<user_id>/<fuser_id>",methods=["GET","POST"])
def funfollow(user_id,fuser_id):
    sql = follower.query.filter_by(user_id=user_id,fuser_id=fuser_id).first()
    db.session.delete(sql)
    db.session.commit()
    return redirect("/follow/"+str(user_id))
# @app.route("/settings/<user_id>")
# def settings(user_id):
#     if request.method == "GET":
#         return render_template("settings.html",user_id=user_id)

@app.route("/edit/<user_id>/<post_id>",methods=["GET","POST"])
def edit(user_id,post_id):
    if request.method == "GET":
        sql = signup.query.filter_by(user_id=user_id).first()
        return render_template("edit.html",user_id=user_id,pic=sql.profile_pic,post_id=post_id)
    elif request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        if title != '' and desc != '':
            sql = post.query.filter_by(post_id=post_id).first()
            sql.title = title
            sql.desc =desc
            db.session.commit()
            sql = post.query.filter_by(post_id=post_id).first()
        elif title == '' and desc =='':
            return redirect("/profile/"+str(user_id))
        elif title == '' and desc != '':
            sql = post.query.filter_by(post_id=post_id).first()
            sql.desc =desc
            db.session.commit()
            sql = post.query.filter_by(post_id=post_id).first()
        elif title != '' and desc == '':
            sql = post.query.filter_by(post_id=post_id).first()
            sql.title =title
            db.session.commit()
            sql = post.query.filter_by(post_id=post_id).first()


        
    return redirect("/profile/"+str(user_id))



@app.route('/delete/<user_id>/<post_id>')
def delete_post(user_id,post_id):
    return render_template('delete_confo.html',user_id=user_id,post_id=post_id)


@app.route('/rdelete/<user_id>/<post_id>')
def rdelete_post(user_id,post_id):

    sql = post.query.filter_by(post_id=post_id).first()
    db.session.delete(sql)
    db.session.commit()
    return redirect("/profile/"+str(user_id))




@app.route('/settings/<user_id>',methods= ["GET","POST"])
def settings(user_id):
    if request.method == "GET":
       
        
        return render_template("settings.html",user_id=user_id)
    elif request.method == "POST":
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        dob = request.form['dob']
        image = request.files["pictureFile"]
    
        sql = signup.query.filter_by(user_id=user_id).first()
        
        # sql.first_name =d['first_name']
        # db.session.commit()
        if fname != '':
            sql.first_name = fname
            db.session.commit()
        if lname != '':
            sql.last_name = lname
            db.session.commit()
        if email != '':
            sql.email = email
            db.session.commit()
        if dob != '':
            sql.dob = dob
            db.session.commit()
        if image.filename != '':
            file_path = "static/"+image.filename
            image.save(file_path)
            sql.profile_pic = image.filename
            db.session.commit()


        
        return redirect('/home/'+str(user_id))
        

@app.route("/like/<post_id>/<user_id>/<fuser_id>")
def like(post_id,user_id,fuser_id):
    sql = post.query.filter_by(post_id=post_id).first()
    if sql.likes:
        c = sql.likes
        c +=1
        sql.likes = c
        db.session.commit()
    else:
        sql.likes = 1
        db.session.commit()
    return redirect('/friend/'+str(user_id)+'/'+str(fuser_id))

@app.route("/like/<post_id>/<user_id>")
def like_home(post_id,user_id):
    sql = post.query.filter_by(post_id=post_id).first()
    if sql.likes:
        c = sql.likes
        c +=1
        sql.likes = c
        db.session.commit()
    else:
        sql.likes = 1
        db.session.commit()
    return redirect('/home/'+str(user_id))
@app.route("/delete_ac/<user_id>")
def delete_ac(user_id):
    
   
    sql3 = user_comment.query.all()
    if sql3:
        for i in sql3:
        
            if str(i.user_id) == str(user_id) or str(i.fuser_id) == str(user_id):
           
                db.session.delete(i)
                db.session.commit()
    sql1 = UserPosts.query.filter_by(user_id=user_id).all()
    if sql1:
        for i in sql1:
        
            sql2 = post.query.filter_by(post_id=i.post_id).first()
     
            if sql2:
                db.session.delete(sql2)
                db.session.commit()
                db.session.delete(i)
                db.session.commit()
    sql5 = follower.query.all()
    if sql5:
        for i in sql5:
            if str(i.user_id) == str(user_id) or str(i.fuser_id) == str(user_id):
           
                db.session.delete(i)
                db.session.commit()
    
    sql = signup.query.filter_by(user_id=user_id).first()
    if sql:
        db.session.delete(sql)
        db.session.commit()
  
   
    return redirect('/login')
