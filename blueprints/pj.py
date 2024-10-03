from flask import Blueprint, render_template, request

bp = Blueprint('pj', __name__, url_prefix='/pj')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'GET':
        return render_template('about.html')
    
