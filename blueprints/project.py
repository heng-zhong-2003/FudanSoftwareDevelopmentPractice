from flask import Blueprint, render_template, request, redirect, url_for,  jsonify, session, flash
from .forms import CreateForm, DeleteForm
from models import ProjectModel, ProjectToUserModel
from exts import db
from .decorators import login_required

bp = Blueprint('pj', __name__, url_prefix='/pj')



@bp.route('/')
def index():
    error = None
    current_page = request.args.get('page', 1)
    projects = ProjectModel.query.all()
    nums_pj = len(projects)
    if current_page <1 or current_page > nums_pj//10+1:  # 404
        i = 1
        error = 'Invalid page number'
    else:
        flash(error)
    return render_template('index.html', projects=projects, i=current_page)

@bp.route('/my_related_projects')
@login_required
def my_related_projects():
    error = None
    current_page = request.args.get('page', 1)
    projects = (db.session.query(ProjectModel)
        .join(ProjectToUserModel, ProjectModel.id == ProjectToUserModel.pj_id)
        .filter(ProjectToUserModel.user_id == session['user_id'])
        .all()
    )
    nums_pj = len(projects)
    if current_page <1 or current_page > nums_pj//10+1:  # 404
        i = 1
        error = 'Invalid page number'
    else:
        flash(error)
    return render_template('my_related_projects.html', projects=projects, i=current_page)


@bp.route('/about/<pj_id>')
@login_required
def about(pj_id):
    project = ProjectModel.query.get(pj_id)

    return render_template('about.html', project=project)

@bp.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('create.html', errors={}, serverError='')
    form = CreateForm(request.form)
    #testing
    
    #
    if form.validate():
        print("Form Data:", request.form)  
        print("name:", form.name.data) 
        print("category:", form.category.data)  
        print("outcome:", form.outcome.data)  
        print("is_private:", form.is_private.data)  
        name = form.name.data
        field = form.field.data
        category = form.category.data
        outcome = form.outcome.data
        if(form.is_private.data=='Public'):
            is_private = False
        else:
            is_private = True

        project = ProjectModel(name=name, field=field, category=category, outcome=outcome, is_private=is_private)
        db.session.add(project)
        db.session.commit()
        pj2user = ProjectToUserModel(user_id = session['user_id'], pj_id = project.id)
        db.session.add(pj2user)
        db.session.commit()
        print('create project success')
        return jsonify({'success': True})
    else:
        # 返回表单验证错误
        print('create project fail')
        return jsonify({'success': False, 'errors': form.errors})

@bp.route("/delete/<int:id>", methods=['GET'])
@login_required
def delete(id):
    project = ProjectModel.query.get(id)
    db.session.delete(project)  # 从会话中删除用户  
    db.session.commit()  # 提交更改到数据库  
    return f'Project {project.name} has been deleted.'

@bp.route("/search/<string:type>:<string:search>",methods=['GET' ,'POST'])
@login_required
def search(type, search):
    current_page = request.form.get('page',1)
    match type:
        case "name":
            projects = ProjectModel.query.filter(ProjectModel.name.like(f'%{search}%'))
        #case ""
    return render_template('index.html', projects=projects, i=current_page)
    
@bp.route('/update/<int:id>', methods=['GET', 'POST'])   
@login_required 
def update(id):
    project = ProjectModel.query.get(id)
    if request.method == 'POST':
        project.name = request.form.get('name')
        project.category = request.form.get('category')
        project.field = request.form.get('field')
        project.outcome = request.form.get('outcome')
        db.session.commit()
    return render_template('about.html', project=project)
    
