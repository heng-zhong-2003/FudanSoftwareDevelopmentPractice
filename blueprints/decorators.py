from functools import wraps
from flask import g, redirect, url_for

def login_required(func):
    # 保留func的元信息
    @wraps(func)
    def check_login(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        return redirect(url_for('auth.login'))
    return check_login
