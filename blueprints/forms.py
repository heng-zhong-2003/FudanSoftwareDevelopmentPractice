import wtforms
import blueprints.authen as authen
from wtforms.validators import Email, Length, EqualTo, AnyOf
from models import UserModel
# 暂时存储验证码的数据库
# from models import EmailCaptchaModel
from exts import db
import models

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
        if user:
            raise wtforms.ValidationError(message="邮箱已经存在!")

    # 验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        # 暂时存储验证码的数据库
        # 从 email_captcha_env 获取验证码对象
        captcha_obj = authen.email_captcha_env.get(email)
        
        # 检查验证码是否存在
        if not captcha_obj:
            raise wtforms.ValidationError("验证码已过期或不存在，请重新获取！")
        
        # 比较验证码值
        if captcha_obj.captcha != captcha:
            raise wtforms.ValidationError("验证码不正确！")
        else:
            # 验证成功后删除验证码记录
            authen.email_captcha_env.pop(email)


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式不正确!")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码长度不正确!")])

class CreateForm(wtforms.Form):
    name = wtforms.StringField(validators=[Length(min=1, max=models.name_max_len, message="项目名称长度不正确")])
    field = wtforms.StringField(validators=[AnyOf(values=['commercial', 'government-sponsored'], message="资金来源格式不正确")])
    # to do
    category = wtforms.StringField(
        validators=[AnyOf(values=['art', 'science', 'military'], message="项目类别不正确!")])
    outcome = wtforms.StringField(validators=[Length(min=0, max=1024, message="成果长度不正确!")])
    is_private = wtforms.BooleanField()

class DeleteForm(wtforms.Form):
    id = wtforms.IntegerField()

class SearchForm(wtforms.Form):
    # Todo
    key_value=''
    