import random
import string
from flask import request, json, Response, Blueprint, g
from flask import current_app as app
from ..models.UserModel import user_model, UserSchema
from ..models.Auth import auth
from ..models.StudyGroup import study_group
from ..views.study_course_view import study_course_shema


user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()


def custom_response(res, status_code):

    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code)


@user_api.route('/create', methods=['POST'])
@auth.auth_required
def create():
    user = user_model.get_one_user(g.user.get('_id'))
    if user.type_of_user != 'admin':
        message = {'error': user.type_of_user}
        return custom_response(message, 400)
    req_data = request.get_json()
    data, _ = user_schema.load(req_data)
    letters = string.ascii_lowercase
    login_gen = ''.join(random.choice(letters) for i in range(10))
    user = user_model(data, login_gen)
    user.save()
#    ser_data = user_schema.dump(user).data
    return custom_response({'login': login_gen}, 200)


@user_api.route('/', methods=['GET'])
def get_a_user():
    login_req = request.args.get('login')
    user = user_model.get_user_by_login(login_req)
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
        return custom_response({'error': 'login'}, 400)
    user = user_model.get_user_by_login(data.get('login'))
    if not user:
        return custom_response({'error': 'invalid credentials1'}, 400)
    if not user.password == data.get('password'):
        return custom_response({'error': 'invalid credentials2'}, 400)
    ser_data = user_schema.dump(user).data
    token = auth.generate_token(ser_data.get('_id'))
    return custom_response({'jwt_token': token}, 200)


@user_api.route('/me', methods=['GET'])
@auth.auth_required
def get_me():
    user = user_model.get_one_user(g.user.get('id'))
    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)


@user_api.route('/group', methods=['GET'])
@auth.auth_required
def get_same_group_students():
    group_id = user_model.get_one_user(g.user.get('_id')).study_group_id
    students = study_group.get_all_students(group_id)
    student_list = []
    for i in students:
        student_list.append(user_schema.dump(i).data)
    return custom_response(student_list, 200)


@user_api.route('/course', methods=['GET'])
@auth.auth_required
def get_same_group_courses():
    group_id = user_model.get_one_user(g.user.get('_id')).study_group_id
    courses = study_group.get_all_courses(group_id)
    course_list = []
    for i in courses:
        course_list.append(study_course_shema.dump(i).data)
    return custom_response(course_list, 200)


@user_api.route('/me', methods=['PUT'])
@auth.auth_required
def update():
    req_data = request.get_json()
    data = user_schema.load(req_data, partial=True)
    return custom_response(str(data), 200)
    user = UserModel.get_one_user(g.user.get('id'))
    user.update(data)
    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)