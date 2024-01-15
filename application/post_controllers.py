from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask import current_app as app
from application.models import signup, post, UserPosts
from .database import db
from base64 import b64encode
import base64
import os




app.config['UPLOAD_FOLDER'] = "static\images"
from datetime import datetime,date





@app.route("/addposts/<user_id>",methods=["GET","POST"])
def add_post(user_id):
    if request.method == "GET":
        sql = signup.query.filter_by(user_id=user_id).first()
        return render_template("addposts.html",user_id=user_id,name=sql.first_name,pic=sql.profile_pic)
    elif request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        now = datetime.now()
       
        image= request.files['pictureFile']
        if image.filename != "":
            file_path = "static/"+image.filename
            image.save(file_path)

            current_time = now.strftime("%H:%M:%S")
           

            current_date = date.today()
            
      
            sql = post(title=title,desc=desc,time=current_time,picture=image.filename,date=current_date)
            db.session.add(sql)
            db.session.commit()
            post_id = sql.post_id
            sql1 = UserPosts(user_id=user_id,post_id=post_id)
            db.session.add(sql1)
            db.session.commit()

            return redirect("/profile/"+str(user_id))
        else:
            user = signup.query.filter_by(user_id=user_id).first()
            user_id = user.user_id

            current_time = now.strftime("%H:%M:%S")
  
            current_date = date.today()
            sql = post(title=title,desc=desc,time=current_time,date=current_date)
            db.session.add(sql)
            db.session.commit()
            post_id = sql.post_id
            sql1 = UserPosts(user_id=user_id,post_id=post_id)
            db.session.add(sql1)
            db.session.commit()

            return redirect("/profile/"+str(user_id))


        
