from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask import current_app as app
from application.models import signup,post,UserPosts,follower,user_comment
from .database import db
import secrets 
from flask_restful import Resource, Api,fields,marshal_with
from flask import make_response
from flask_restful import reqparse 
from werkzeug .exceptions import HTTPException
import json
app.secret_key = secrets.token_hex()
class NotFoundError(HTTPException):
    def __init__(self,status_code):
        self.response = make_response('',status_code)
class BuisnessValidationError(HTTPException):
    def __init__(self,status_code,error_code,error_message):
        message = {'error_code':error_code,'error_message':error_message}
        self.response = make_response(json.dumps(message),status_code)
create_signup_parser = reqparse.RequestParser()      
create_signup_parser.add_argument('user_name')
create_signup_parser.add_argument('first_name')
create_signup_parser.add_argument('user_id')
create_signup_parser.add_argument('password')
create_signup_parser.add_argument('last_name')
create_signup_parser.add_argument('email')
create_signup_parser.add_argument('dob')
update_signup_parser = reqparse.RequestParser()
update_signup_parser.add_argument('first_name')
update_signup_parser.add_argument('last_name')
update_signup_parser.add_argument('email')
update_signup_parser.add_argument('dob')
update_signup_parser.add_argument('profile_pic')

output_fields = {"user_id": fields.Integer,"user_name": fields.String,
"first_name": fields.String, "last_name": fields.String,"email":fields.String,"dob":fields.String,"password":fields.String,"profile_pic":fields.String}
class SignupAPI(Resource):
    @marshal_with(output_fields)
    def get(self,user_name):
        sql = db.session.query(signup).filter(signup.user_name == user_name).first()
        if sql:
            return sql
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(output_fields)
    def post(self):
        args = create_signup_parser.parse_args()
        user_id = args.get("user_id",None)
        user_name = args.get("user_name",None)
        first_name = args.get("first_name",None)
        last_name = args.get("last_name",None)
        email = args.get("email",None)
        dob = args.get("dob",None)
        password = args.get("password",None)
        profile_pic = args.get("profile_pic",None)
        if not user_id :
            raise  BuisnessValidationError(status_code=404, error_code ='USER001',error_message = 'User id is required')
        if user_name == None:
            raise  BuisnessValidationError(status_code=404, error_code ='USER002',error_message = 'User Name is required')

        if first_name is None:
            raise  BuisnessValidationError(status_code=404, error_code ='USER005',error_message = 'First Name is required')
        if last_name is None:
            raise  BuisnessValidationError(status_code=404, error_code ='USER006',error_message = 'Last Name is required')
        if password is None:
            raise  BuisnessValidationError(status_code=404, error_code ='USER003',error_message = 'Password is required')
        if email is None:
            raise  BuisnessValidationError(status_code=404, error_code ='USER004',error_message = 'Email is required')
        
        else:
            sql = signup(user_id=user_id,user_name= user_name,first_name=first_name,last_name=last_name,dob=dob,password=password,email=email)
            db.session.add(sql)
            db.session.commit()
            return  sql
    @marshal_with(output_fields)
    def put(self,user_name):
        args = update_signup_parser.parse_args()
        
        first_name = args.get("first_name",None)
        last_name = args.get("last_name",None)
        email = args.get("email",None)
        dob = args.get("dob",None)
        profile_pic = args.get("profile_pic",None)
        course_description = args.get("course_description",None)
        if user_name is None:
            return NotFoundError(status_code=404)
        
        else:
            sql = db.session.query(signup).filter(signup.user_name == user_name).first()
            if sql is None:
                raise NotFoundError(status_code=404)
            if first_name is not None:
                sql.first_name = first_name
            if last_name is not None:
                sql.last_name = last_name
            if dob is not None:
                sql.dob = dob
            if email is not None:
                sql.email = email
            if profile_pic is not None:
                sql.profile_pic = profile_pic

            db.session.commit()
            return  sql
    
    def delete(self,user_name):
   
        sql45 = signup.query.filter_by(user_name=user_name).first()
        if not sql45:
            raise NotFoundError(status_code=404)
        user_id=sql45.user_id
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
            return "Successfully Deleted", 200
        else:
            raise NotFoundError(status_code=404)
    # def delete(self,user_name):
        
    #     sql = signup.query.filter_by(user_name=user_name).first()
    #     if sql is None:
    #          raise NotFoundError(status_code=404)
    #     user_id = sql.user_id
    #     sql1 = user_comment.query.all()
    #     if sql1:
    #         for i in sql:
    #             if str(i.user_id)== str(user_id) or str(fuser_id) == str(user_id):
    #                 db.session.delete(i)
    #                 db.session.commit()
    #     sql2 = UserPosts.query.filter_by(user_id=user_id).all()
    #     for i in sql2:
    #         sql3 = post.query.filter_by(post_id=i.post_id).first()
            
    #         db.session.delete(i)
    #         db.session.commit()
    #         db.session.delete(sql3)
    #         db.session.commit()
    #     sql4 = follower.query.all()
    #     for i in sql4:
    #         if str(i.user_id)== str(user_id) or str(i.fuser_id) == str(user_id):
    #             db.session.delete(i)
    #             db.session.commit()

    #     sql5 = signup.query.filter_by(user_id=user_id).first()
    #     db.session.delete(sql5)
    #     db.session.commit()

    #     return "",200

create_post_parser = reqparse.RequestParser()   
create_post_parser.add_argument('user_name')
create_post_parser.add_argument('title')
create_post_parser.add_argument('desc')
create_post_parser.add_argument('time')
create_post_parser.add_argument('post_id')
create_post_parser.add_argument('date')
create_post_parser.add_argument('picture')
create_post_parser.add_argument('likes')

update_post_parser = reqparse.RequestParser()

update_post_parser.add_argument('title')
update_post_parser.add_argument('desc')
update_post_parser.add_argument('picture')



output_fields = { 
"post_id": fields.Integer, "title": fields.String,"desc":fields.String,"time":fields.String,"date":fields.String,
"picture":fields.String}
class PostAPI(Resource):
    @marshal_with(output_fields)
    def get(self,user_name):
        sql = db.session.query(signup).filter(signup.user_name == user_name).first()
        if not sql:
            raise NotFoundError(status_code=404)

        user_id=sql.user_id
        sql3 = db.session.query(UserPosts).filter_by(user_id=user_id).all()
        l = []
        if sql3:
            for i in sql3:
                sql4 = db.session.query(post).filter_by(post_id=i.post_id).first()
                l.append(sql4)
     
      
            return l
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(output_fields)
    def post(self,user_name):
        args = create_post_parser.parse_args()
       
        title = args.get("title",None)
        desc = args.get("desc",None)
        time = args.get("time",None)
        date = args.get("date",None)
        picture = args.get("picture",None)
     
        if title is None:
            raise  BuisnessValidationError(status_code=404, error_code ='POST001',error_message = 'Post Title is required')
        if desc is None:
            raise  BuisnessValidationError(status_code=404, error_code ='POST002',error_message = 'Post description is required')

        if date is None:
            raise  BuisnessValidationError(status_code=404, error_code ='POST003',error_message = 'Date is required')
        if time is None:
            raise  BuisnessValidationError(status_code=404, error_code ='POST004',error_message = 'Time is required')
       
        
        else:
            sql = post(title=title,desc=desc,picture=picture,time=time,date=date)
            db.session.add(sql)
            
            db.session.commit()
            post_id = sql.post_id
            sql5 = signup.query.filter_by(user_name=user_name).first()
            if sql5:
                sql2 = UserPosts(user_id=sql5.user_id,post_id=post_id)
                db.session.add(sql2)
                db.session.commit()
            
                return  sql
            else:
                return "", 400
    
    @marshal_with(output_fields)
    def put(self,user_name,post_id):
        args = update_post_parser.parse_args()
        title = args.get("title",None)
        desc = args.get("desc",None)
        picture = args.get("picture",None)
        sql2 = signup.query.filter_by(user_name=user_name).first()
        sql3 = post.query.filter_by(post_id=post_id).first()
        if not sql2:
            raise NotFoundError(status_code=404)
        if not sql3:
            raise NotFoundError(status_code=404)      
        sql = post.query.filter_by(post_id=post_id).first()
        if title:
            sql.title = title
        if desc:
            sql.desc = desc
        if picture:
            sql.picture = picture
        db.session.add(sql)
        db.session.commit()
        return sql
    
    def delete(self,user_name,post_id):
        sql1 = signup.query.filter_by(user_name=user_name).first()
        sql2 = post.query.filter_by(post_id=post_id).first()
        if not sql1:
            raise NotFoundError(status_code=404)
        if not sql2:
            raise NotFoundError(status_code=404)
        sql = post.query.filter_by(post_id=post_id).first()
        db.session.delete(sql)
        db.session.commit()
        return "",200

    



