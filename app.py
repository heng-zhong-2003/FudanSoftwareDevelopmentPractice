from flask import Flask, request, render_template, session, g
import config
from exts import db, mail
from models import UserModel
from blueprints.auth import bp as auth_bp
from blueprints.project import bp as pj_bp
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

# blueprint 模块化
app.register_blueprint(auth_bp)
app.register_blueprint(pj_bp)

# hook
@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)

@app.context_processor
def context_processor():
    return {"user": g.user}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

