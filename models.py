from exts import db

name_max_len = 500
field_max_len = 50
category_max_len = 100
outcome_max_len = 1024

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    
class ProjectModel(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(name_max_len), nullable=False)
    field = db.Column(db.String(field_max_len), nullable=False)
    category = db.Column(db.String(category_max_len), nullable=False)
    outcome = db.Column(db.String(outcome_max_len), nullable=False)
    is_private = db.Column(db.Boolean, nullable=False, default=False)
    #create_time = db.Column(db.DateTime, nullable=False)
    #外键
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 反向引用
    #user = db.relationship('UserModel', backref=db.backref('projects'))

class ProjectToUserModel(db.Model):
    __tablename__ = 'project2user'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    pj_id = db.Column(db.Integer,db.ForeignKey('project.id'), primary_key=True)

# 暂时使用数据库存储验证码
# class EmailCaptchaModel(db.Model):
#     __tablename__ = 'email_captcha'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     email = db.Column(db.String(50), nullable=False)
#     captcha = db.Column(db.String(10), nullable=False)
#     # 定期清理
#     # used = db.Column(db.Boolean, default=False)
