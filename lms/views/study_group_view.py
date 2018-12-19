from flask import request, json, Response, Blueprint, g
from ..models.StudyGroup import study_group, StudyGroupShema
from ..models.UserModel import user_model
from ..models.Auth import auth


study_group_api = Blueprint('study_group_api', __name__)
study_group_shema = StudyGroupShema()


@study_group_api.route('/create', methods=['POST'])
@auth.auth_required
def create():
    uid = g.user.get('_id')
    user = user_model.get_one_user(uid)
    if user.type_of_user != 'admin':
        message = {'error': user.type_of_user}
        return custom_response(message, 400)
    req_data = request.get_json()
    data, error = study_group_shema.load(req_data)
    if error:
        return custom_response(error, 400)
    group = study_group(data)
    group.save()
    data = study_group_shema.dump(group).data
    return custom_response(data, 200)


def custom_response(res, status_code):

    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code)
