from flask import request, json, Response, Blueprint, g
from ..models.StudyGroup import StudyGroup, StudyGroupShema
from ..models.UserModel import UserModel, UserSchema
from ..models.Auth import Auth
from functools import wraps


study_group_api = Blueprint('study_group_api', __name__)
study_group_shema = StudyGroupShema()

@study_group_api.route('/create', methods=['POST'])
@Auth.auth_required
def create():
    uid = g.user.get('id')
    user = UserModel.get_one_user(uid)
    if user.type_of_user != 'admin':
        message = {'error':user.type_of_user}
    req_data = request.get_json()   
    data, error = study_group_shema.load(req_data)
    if error:
        return custom_response(error, 400)
    group = StudyGroup(data)
    group.save()
    data = study_group_shema.dump(group).data
    return custom_response(data, 200)
    return custom_response(group.study_course, 200)



def custom_response(res, status_code):

    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
      )
