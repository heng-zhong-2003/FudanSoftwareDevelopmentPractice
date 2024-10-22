from flask import Blueprint, render_template, request, redirect, url_for,  jsonify, session
from .forms import RegisterForm, LoginForm, CreateForm, DeleteForm
from models import ProjectModel
from exts import db
bp = Blueprint('pj', __name__, url_prefix='/pj')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'GET':
        return render_template('about.html')

@bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html', errors={}, serverError='')
    form = CreateForm(request.form)
    #testing
    print("Form Data:", request.form)  
    print("name:", form.name.data) 
    print("category:", form.category.data)  
    print("outcome:", form.outcome.data)  
    print("is_private:", form.is_private.data)  
    #
    if form.validate():
        name = form.name.data
        field = form.field.data
        category = form.category.data
        outcome = form.outcome.data
        is_private = form.is_private.data

        project = ProjectModel(name=name, field=field, category=category, outcome=outcome, is_private=is_private)
        db.session.add(project)
        db.session.commit()
        return jsonify({'success': True})
    else:
        # 返回表单验证错误
        return jsonify({'success': False, 'errors': form.errors})

@bp.route("/delete", methods=['DELETE'])
def delete():
    if request.method == 'DELETE':
        return render_template('delete.html')
    form = DeleteForm(delete.form)
    if form.validate():
        pj_id = form.id.data
    project = ProjectModel.query.get(pj_id)
    db.session.delete(project)  # 从会话中删除用户  
    db.session.commit()  # 提交更改到数据库  
    return f'Project {project.name} has been deleted.'

@bp.route("/search", methods=['GET','POST'])
def search():
    if request.method == 'DELETE':
        return render_template('delete.html')
    
    
    
