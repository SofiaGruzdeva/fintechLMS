from flask import request, json, Response, Blueprint, g
from ..models.StudyGroup import study_group
from ..models.StudyCourse import study_course, StudyCourseShema
from ..models.UserModel import user_model
from ..models.Auth import auth
from .shared import custom_response

study_course_api = Blueprint('study_course_api', __name__)
study_course_shema = StudyCourseShema()


@study_course_api.route('/create', methods=['POST'])
@auth.auth_required
@auth.admin_required
def create():
    req_data = request.get_json()
    data, error = study_course_shema.load(req_data)
    if error:
        return custom_response(error, 400)
    course = study_course(data)
    course.save()
    data = study_course_shema.dump(course).data
    return custom_response(data, 200)


@study_course_api.route('/add_group', methods=['POST'])
@auth.auth_required
@auth.admin_required
def add_group():
    req_data = request.get_json()
    group = study_group.get_one_group(req_data['study_group_id'])
    course = study_course.get_one_course(req_data['study_course_id'])
    course.add_group(group)
#     data, error = study_course_shema.load(req_data)
#     if error:
#         return custom_response(error, 400)
#     course = StudyCourse(data)
#     course.save()
    data = study_course_shema.dump(group).data
    return custom_response(data, 200)


@study_course_api.route('/add_teacher', methods=['POST'])
@auth.auth_required
@auth.admin_required
def add_teacher():
    req_data = request.get_json()
    teacher = user_model.get_one_user(req_data['teacher_id'])
    course = study_course.get_one_course(req_data['study_course_id'])
    course.add_teacher(teacher)
#     data, error = study_course_shema.load(req_data)
#     if error:
#         return custom_response(error, 400)
#     course = StudyCourse(data)
#     course.save()
    data = study_course_shema.dump(course).data
    return custom_response(data, 200)
