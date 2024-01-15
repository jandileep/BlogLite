from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask import current_app as app
from application.models import signup, post, UserPosts,user_comment,follower
from .database import db
import secrets 
from base64 import b64encode
import base64
import random
app.secret_key = secrets.token_hex()
app.config['UPLOAD_FOLDER'] = "static\images"




app.secret_key = secrets.token_hex()
@app.route("/home/<user_id>",methods=["GET","POST"])
def home(user_id):
    sql = signup.query.filter_by(user_id=user_id).first()
    #name = sql.user_name
    if sql:
        if('user' in session and session['user'] == sql.user_id):
            sql4 = post.query.all()
            rand_post = []
            stm = follower.query.filter_by(user_id=user_id).all()
            list1 = []
            for i in stm:
                list1.append(i.fuser_id)
            list2 = []
            for i in list1:
                stm2 = UserPosts.query.filter_by(user_id=i).all()
                for i in stm2:
                    stm3 = post.query.filter_by(post_id=i.post_id).first()
                    
                    k = stm3.time
                    m = k[:2]+k[3:5]+k[6:]
                    # return m
                    d = stm3.date
                    dm = d[:4]+d[5:7]+d[8:]
                    list2.append((i.post_id,int(m),int(dm)))
            
            from operator import itemgetter
            list2 = sorted(list2,key=itemgetter(1))
            list2 = sorted(list2,key=itemgetter(2))   
            list2.reverse()
            for i in list2:
                rand_post.append(i[0])
            
            post_list = []
            for p in rand_post:
                sql1 = post.query.filter_by(post_id=p).first()
                sql2 = UserPosts.query.filter_by(post_id=p).first()
                sql3 = signup.query.filter_by(user_id=sql2.user_id).first()
                
              
                puser_name = sql3.user_name
                dp = sql3.profile_pic
                post_list.append([puser_name,dp,sql1.post_id, str(sql2.user_id),sql1.title,sql1.desc,sql1.time,sql1.picture,sql1.likes,sql1.date])

            com_list = []
            sql5 = user_comment.query.all()
            
            

            for i in sql5:
                sql2 = signup.query.filter_by(user_id=i.user_id).first()
                com_list.append([sql2.user_name,i.user_id, i.post_id, i.comment,sql2.profile_pic])

            
            #-------------------------------------
            sql2 = follower.query.all()
            t = []
            for i in sql2:
                t.append([i.user_id,i.fuser_id])
            ser_user = request.args.get('user_name')
            l = []
            if ser_user:
                ori_user = signup.query.filter(signup.user_name.contains(ser_user)).all()
                if ori_user:
                  
                    return render_template("search.html",user=ori_user,user_id=int(user_id),t=t)
            return render_template("home.html",user_id=user_id,name=sql.first_name,pic=sql.profile_pic,post_list=post_list,com_list=com_list)
    return "Session expired. Please Login Again"
  


@app.route("/signup",methods=["GET","POST"])
def temp2():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form["user_name"]
        fname= request.form["first_name"]
        lname= request.form['last_name']
        pwd = request.form['pwd']
        dob = request.form['dob']
        email_id = request.form['email_id']
        image = request.files["pictureFile"]
        # if image.filename != "":
        
        file_path = "static/"+image.filename
        image.save(file_path)
        sql5 = signup.query.filter_by(email=email_id).first()
        if sql5:
            return render_template("sorry.html",choice=3)
        else:
            sql = signup(user_name=username,first_name=fname,last_name=lname,password=pwd,dob=dob,email=email_id,profile_pic=image.filename)
            db.session.add(sql)
            db.session.commit()
            # sql1 = follower(user_id=sql.user_id,fuser_id=)
            # db.session.add(sql1)
            # db.session.commit()
  
            return render_template("login.html")
            
        

           
    
@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email_id = request.form['email']
        password= request.form["pwd"]
        
        sql3 = db.session.query(signup).filter(signup.email == email_id).first()
        if sql3:
        

            if password == sql3.password:
                name1 = sql3.first_name
                session["user"] = sql3.user_id

                #return render_template('home.html',name=name1,user_id=sql3.user_id)
                return redirect(url_for("home",user_id=sql3.user_id))#name=sql3.user_name
            else:
                return render_template("invalid.html",choice=1)
        else:
            return render_template("invalid.html",choice=2)
          
    return render_template("login.html")  

@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop("user")
    return redirect(url_for(login))

@app.route('/dummy')
def newhome():
    sql4 = post.query.all()
    rand_post = []
    for i in sql4:
        rand_post.append(i.post_id)
    random.shuffle(rand_post)
    post_list = []
    for p in rand_post:
        sql1 = post.query.filter_by(post_id=p).first()
        sql2 = UserPosts.query.filter_by(post_id=p).first()
        sql3 = signup.query.filter_by(user_id=sql2.user_id).first()
        puser_name = sql3.user_name
        post_list.append([puser_name,sql1.post_id, sql2.user_id,sql1.title,sql1.desc,sql1.time,sql1.picture])

    comment_list = []
    sql = user_comment.query.all()
    for i in sql:
        sql2 = signup.query.filter_by(user_id=i.user_id).first()
        comment_list.append([sql2.user_name,i.user_id, i.post_id, i.comment])
    #return post_list
    return (comment_list)