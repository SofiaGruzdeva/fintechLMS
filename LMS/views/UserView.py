import random
import string
from marshmallow import Schema, fields
# from ..models.UserModel import UserModel
from functools import wraps
from flask import request, json, Response, Blueprint, g
# app = Flask(__name__)
from ..models.UserModel import UserModel, UserSchema
from ..models.Auth import Auth
from ..models.StudyGroup import StudyGroup
from ..views.StudyCourseView import study_course_shema
from flask import current_app as app
# app.config.update(
# #    DATABASE=r"C:\\Users\\admin\\Fintech\\LMS1\\db.db",
#     SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
#     USERNAME='admin',
#     PASSWORD='default', 
#     JWT_SECRET_KEY = 'hhgaghhgsdhdhdd',
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Users\\admin\\Fintech\\LMS1\\db.db'
# )

# db = SQLAlchemy(app)


user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()

def custom_response(res, status_code):

    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )



@user_api.route('/create', methods=['POST'])
#@Auth.auth_required
def create():
#     user = UserModel.get_one_user(g.user.get('id'))
#     if user.type_of_user != 'admin':
#         message = {'error':user.type_of_user}
#         return custom_response(message, 400)
    req_data = request.get_json()
    data, error = user_schema.load(req_data)
#     user_in_db = UserModel.get_user_by_email(data.get('email'))
#     if user_in_db:
#         message = {'error': 'User already exist, please supply another email address'}
#         return custom_response(message, 400)
#    g.user.get('id')
    letters = string.ascii_lowercase
    login = ''.join(random.choice(letters) for i in range(10))
#    if req_data['type_of_user'] == 'student':
#        data['study_group_id'] = uid
    user = UserModel(data, login)
    a = user.save()
    ser_data = user_schema.dump(user).data

#     token = Auth.generate_token(ser_data.get('id'))
    return custom_response({'login':login}, 200)




@user_api.route('/', methods=['GET'])
def get_a_user():
    login = request.args.get('login')
    user = UserModel.get_user_by_login(login)
    if not user:
        return custom_response({'error': 'user not found'}, 404)
  
    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)



@user_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    data, error = user_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    if not data.get('login') or not data.get('password'):
        return custom_response({'error': 'you need login and password to sign in'}, 400)
    user = UserModel.get_user_by_login(data.get('login'))
    if not user:
        return custom_response({'error': 'invalid credentials1'}, 400)
    if not user.password == data.get('password'):
        return custom_response({'error': 'invalid credentials2'}, 400)
    ser_data = user_schema.dump(user).data
    token = Auth.generate_token(ser_data.get('id'))
    return custom_response({'jwt_token': token}, 200)
#    return custom_response({'jwt_token': app.config.get('JWT_SECRET_KEY')}, 200)



@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
    user = UserModel.get_one_user(g.user.get('id'))
    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)



@user_api.route('/group', methods=['GET'])
@Auth.auth_required
def get_same_group_students():
    group_id = UserModel.get_one_user(g.user.get('id')).study_group_id
    students = StudyGroup.get_all_students(group_id)
    student_list = []
    for i in students:
        student_list.append(user_schema.dump(i).data)
        
#    ser_user = user_schema.dump(user).data
    return custom_response(student_list, 200)


@user_api.route('/course', methods=['GET'])
@Auth.auth_required
def get_same_group_courses():
    group_id = UserModel.get_one_user(g.user.get('id')).study_group_id
    courses = StudyGroup.get_all_courses(group_id)
    course_list = []
    for i in courses:        
        course_list.append(study_course_shema.dump(i).data)        
#    ser_user = user_schema.dump(user).data
    return custom_response(course_list, 200)


