from flask import request, json, Response, Blueprint, g
from ..models.StudyGroup import StudyGroup, StudyGroupShema
from ..models.StudyCourse import StudyCourse, StudyCourseShema
from ..models.UserModel import UserModel, UserSchema
from ..models.Auth import Auth
from functools import wraps

study_course_api = Blueprint('study_course_api', __name__)
study_course_shema = StudyCourseShema()

@study_course_api.route('/create', methods=['POST'])
@Auth.auth_required
def create():
    uid = g.user.get('id')
    user = UserModel.get_one_user(uid)
    if user.type_of_user != 'admin':
        message = {'error':user.type_of_user}
    req_data = request.get_json()   
    data, error = study_course_shema.load(req_data)
    if error:
        return custom_response(error, 400)
    course = StudyCourse(data)
    course.save()
    data = study_course_shema.dump(course).data
    return custom_response(data, 200)


@study_course_api.route('/add_group', methods=['POST'])
@Auth.auth_required
def add_group():
    uid = g.user.get('id')
    user = UserModel.get_one_user(uid)
    if user.type_of_user != 'admin':
        message = {'error':user.type_of_user}
    req_data = request.get_json()   
    group = StudyGroup.get_one_group(req_data['study_group_id'])
    course = StudyCourse.get_one_course(req_data['study_course_id'])
    course.add_group(group)
#     data, error = study_course_shema.load(req_data)
#     if error:
#         return custom_response(error, 400)
#     course = StudyCourse(data)
#     course.save()
    data = study_course_shema.dump(group).data
    return custom_response(data, 200)


@study_course_api.route('/add_teacher', methods=['POST'])
@Auth.auth_required
def add_teacher():
    uid = g.user.get('id')
    user = UserModel.get_one_user(uid)
    if user.type_of_user != 'admin':
        message = {'error':user.type_of_user}
    req_data = request.get_json()   
    teacher = UserModel.get_one_user(req_data['teacher_id'])
    course = StudyCourse.get_one_course(req_data['study_course_id'])
    course.add_teacher(teacher)
#     data, error = study_course_shema.load(req_data)
#     if error:
#         return custom_response(error, 400)
#     course = StudyCourse(data)
#     course.save()
    data = study_course_shema.dump(course).data
    return custom_response(data, 200)


def custom_response(res, status_code):

    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
      )