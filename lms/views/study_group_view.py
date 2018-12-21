from flask import request, json, Response, Blueprint, g
from ..models.StudyGroup import study_group, StudyGroupShema
from ..models.UserModel import user_model
from ..models.Auth import auth
from .shared import custom_response

study_group_api = Blueprint('study_group_api', __name__)
study_group_shema = StudyGroupShema()


@study_group_api.route('/create', methods=['POST'])
@auth.auth_required
@auth.admin_required
def create():
    req_data = request.get_json()
    data, error = study_group_shema.load(req_data)
    if error:
        return custom_response(error, 400)
    group = study_group(data)
    group.save()
    data = study_group_shema.dump(group).data
    return custom_response(data, 200)
