import pytest
from app import app, db  # 导入你的Flask应用
from models import UserModel

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def init_database():
    with app.app_context():
        db.create_all()  # 创建所有表
        test_user = UserModel(username='Hellen', email='test@example.com', password='hashed_password')  # 使用合适的哈希密码
        db.session.add(test_user)
        db.session.commit()
        yield
        #db.drop_all()  # 清理测试数据库

@pytest.mark.usefixtures('client')
def test_register_success(client):
    response = client.post('/auth/register', data={'email': 'test@example.com', 'password': 'hashed_password', 'username': 'Hellen', 'password_confirm':'hashed_password'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True

@pytest.mark.usefixtures('client')
def test_login_invalid_form_data(client):
    response = client.post('/auth/login', data={'email': '', 'password': ''})  # 提交空数据
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['message'] == "Invalid form data"
    assert 'email' in json_data['errors']  # 检查是否包含表单错误

@pytest.mark.usefixtures()
def test_login_invalid_credentials(client):
    response = client.post('/auth/login', data={'email': 'test@example.com', 'password': 'wrong_password'})
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['message'] == "邮箱或密码错误"

@pytest.mark.usefixtures()
def test_login_success(client):
    response = client.post('/auth/login', data={'email': 'test@example.com', 'password': 'hashed_password'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == "Login successful!"
    assert json_data['success'] is True
