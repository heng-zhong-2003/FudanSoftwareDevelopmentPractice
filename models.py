from exts import db

field_max_len = 50
category_max_len = 100
outcome_max_len = 1024

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    
class ProjectModel(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field = db.Column(db.String(field_max_len), nullable=False)
    category = db.Column(db.String(category_max_len), nullable=False)
    outcome = db.Column(db.String(outcome_max_len), nullable=False)
    is_privary = db.Column(db.Boolean, nullable=False, default=False)

# 暂时使用数据库存储验证码
class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    captcha = db.Column(db.String(10), nullable=False)
    # 定期清理
    # used = db.Column(db.Boolean, default=False)
    