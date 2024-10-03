import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import UserModel
# 暂时存储验证码的数据库
from models import EmailCaptchaModel
from exts import db

# 验证提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email= wtforms.StringField(validators=[Email(message="邮箱格式不正确!")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码不正确!")])
    username = wtforms.StringField(validators=[Length(min=6, max=20, message="用户名长度不正确!")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码长度不正确!")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致!")])

    # 自定义验证
    # 邮箱是否已经存在
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user: raise wtforms.ValidationError(message="邮箱已经存在!")

    # 验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        # 暂时存储验证码的数据库
        EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not EmailCaptchaModel: raise wtforms.ValidationError(message="验证码不正确!")
        # todo: 删除验证码
        # else: 
        #     db.session.delete(captcha)
        #     db.session.commit()

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式不正确!")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码长度不正确!")])
