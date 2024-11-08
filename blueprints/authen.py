from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
import string, random, time
from .forms import RegisterForm, LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
# 暂时数据库存储验证码
# from models import EmailCaptchaModel
bp = Blueprint('auth', __name__, url_prefix='/auth')

# 验证码有效的秒数，30 分钟
captcha_valid_time = 30 * 60

class CaptchaWithTime:
    def __init__(self, captcha: str, time_stamp: float) -> None:
        self.captcha = captcha
        self.time_stamp = time_stamp

email_captcha_env: dict[str, CaptchaWithTime] = dict()

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', errors={}, serverError='')
    
    form = LoginForm(request.form)
    print("Form Data:", request.form)  # 打印整个表单数据字典
    print("Email:", form.email.data)  # 打印特定字段（例如 username）
    print("Password:", form.password.data)  # 打印特定字段（例如 password）
    if form.validate():
        email = form.email.data
        input_password = form.password.data
        user = UserModel.query.filter_by(email = email).first() 
        if user and check_password_hash(user.password, input_password):
            session['user_id'] = user.id
            return jsonify({"message": "Login successful!", 'success': True}), 200  # 返回成功消息
        else:
            return jsonify({"message": "邮箱或密码错误", 'success': True}), 400  # 返回失败消息
    else:
        return jsonify({"message": "Invalid form data", "errors": form.errors}), 400  # 返回验证错误
    

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', errors={}, serverError='')
    
    # 创建表单对象
    form = RegisterForm(request.form)
    print("Form Data:", request.form)  # 打印整个表单数据字典
    print("Username:", form.username.data)  # 打印特定字段（例如 username）
    print("Password:", form.password.data)  # 打印特定字段（例如 password）
    print("Email:", form.email.data)  # 打印特定字段（例如 email）

    if form.validate():
        # 提取表单数据
        email = form.email.data
        username = form.username.data
        password = form.password.data
        
        # 创建新用户并保存到数据库
        user = UserModel(email=email, username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        # 返回成功消息
        return jsonify({'success': True})
    else:
        # 返回表单验证错误
        return jsonify({'success': False, 'errors': form.errors})


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# TODO: 全局创建一个 email * (captcha, timestamp_at_creation) dict
# 每次这个函数（发送验证码）被调用，都把这个用户的 email 和生成的验证码
# 推到这个 dict 中。每次验证，比较：
# 1. 验证码是否正确
# 2. 验证码是否过期（用户发送的和 dict 中存储的 timestamp 差）
# 每次调用，扫遍这个 dict，删掉过期的验证码项
@bp.route("/captcha/email", methods=['POST'])
def email_captcha():
    # email = request.args.get("email")
    email = request.json.get("email")
    source = string.digits*4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)
    message = Message(subject='注册验证码', recipients=[email], body='你的验证码是：'+captcha)
    print(message)

    try:
        mail.send(message)
    except Exception as e:
        # 邮件发送失败
        return jsonify({"code": 500, "message": f"Failed to send email: {str(e)}", "data": None})
    
    '''
    todo: redis
    1. 保存验证码到数据库
    2. 验证码有效时间
    '''
    curr_time = time.time()
    # 邮箱和 (当前验证码, 当前时间) 放到全局 dict
    email_captcha_env[email] = CaptchaWithTime(
        captcha=captcha,
        time_stamp=curr_time,
    )
    # 过期的 (邮箱, 验证码) 删掉。应该是不能边遍历边 mutate 容器的，所以我写了两个 for
    keys_to_delete = []
    for em, cap in email_captcha_env.items():
        if curr_time - cap.time_stamp > captcha_valid_time:
            keys_to_delete.append(em)
    for em in keys_to_delete:
        email_captcha_env.pop(em)
    # RESTful API
    # {code:200/400/500, message:"", data:{}}
    return jsonify({"code":200, "message":"", "data":None})

@bp.route("/mail/test")
def test_mail():
    message = Message(subject='邮箱测试', recipients=['@qq.com'], body='测试邮件')
    mail.send(message)
    return '邮件发送成功！'
