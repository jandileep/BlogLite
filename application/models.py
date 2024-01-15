from .database import db


class signup(db.Model):
    __tablename__ = 'signup'
    user_id = db.Column(db.Integer,autoincrement = True, primary_key = True)
    first_name = db.Column(db.String,nullable = False)
    user_name = db.Column(db.String,nullable=False,unique=True)
    last_name = db.Column(db.String,nullable = False)
    password = db.Column(db.String, nullable = False)
    dob = db.Column(db.String, nullable= False)
    email = db.Column(db.String, nullable = False,unique=True)
    profile_pic = db.Column(db.Text)
    user_signup_id = db.relationship('post',secondary='user_post',cascade="all, delete-orphan",single_parent=True )

class post(db.Model):
    __tablename__ = 'Post'
    post_id = db.Column(db.Integer,autoincrement=True,primary_key = True)
    title = db.Column(db.String, nullable=False)
    time = db.Column(db.String,nullable = False)
    desc = db.Column(db.String,nullable=False)
    picture = db.Column(db.Text)
    likes = db.Column(db.Integer)
    date = db.Column(db.String,nullable=False)

    
    # user_post_id = db.relationship("signup",secondary="user_post")

class UserPosts(db.Model):
    __tablename__ = "user_post"
    user_id = db.Column(db.Integer, db.ForeignKey("signup.user_id"), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey("Post.post_id"), nullable = False)
    user_userpost_id = db.Column(db.Integer, primary_key = True, autoincrement = True)

class follower(db.Model):
    __tablename__ = "follow"
    user_id = db.Column(db.Integer,db.ForeignKey("signup.user_id"),nullable=False)
    fuser_id = db.Column(db.Integer,db.ForeignKey("signup.user_id"),nullable=False)
    user_follow_id = db.Column(db.Integer,primary_key=True,autoincrement=True)

class user_comment(db.Model):
    __tablename__ = "comment"
    user_id = db.Column(db.Integer,db.ForeignKey("signup.user_id"),nullable=False)
    fuser_id = db.Column(db.Integer,db.ForeignKey("signup.user_id"),nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey("Post.post_id"),nullable=False)
    comment_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    comment = db.Column(db.String,nullable=False)

    

'''class user_like(db.Model):
    __table__ = "user_like"
    user_id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer)
    like_id = db.Column(db.Integer,autoincrement=True)'''
db.create_all() 
