import datetime
from functools import wraps
from flask import json, Response, request, g
from flask import current_app as app
import jwt
from ..models.UserModel import user_model
from ..views.shared import custom_response


class auth():
    @staticmethod
    def generate_token(user_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
            }
        return jwt.encode(
            payload,
            app.config.get('JWT_SECRET_KEY'),
            'HS256'
        ).decode("utf-8")

    @staticmethod
    def decode_token(token):
        res = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, app.config.get('JWT_SECRET_KEY'))
            res['data'] = {'user_id': payload['sub']}
            return res
        except jwt.ExpiredSignatureError:
            res['error'] = {'message': 'token expired, please login again'}
            return res
        except jwt.InvalidTokenError:
            message = 'Invalid token, please try again with a new token'
            res['error'] = {'message': message}
            return res

    @staticmethod
    def auth_required(func):
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            er = 'please login'
            error = 'user does not exist, invalid token'
            if 'api-token' not in request.headers:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': er}),
                    status=400
                )
            token = request.headers.get('api-token')
            data = auth.decode_token(token)
            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )

            user_id = data['data']['user_id']
            check_user = user_model.get_one_user(user_id)
            if not check_user:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': error}),
                    status=400
                )
            g.user = {'_id': user_id}
            return func(*args, **kwargs)
        return decorated_auth

    @staticmethod
    def admin_required(func):
        @wraps(func)
        def decorated_admin(*args, **kwargs):
            token = request.headers.get('api-token')
            data = auth.decode_token(token)
            user_id = data['data']['user_id']
            user = user_model.get_one_user(user_id)
            admin_flg, error = user.is_admin()
            if not admin_flg:
                return custom_response(str(error), 400)
            return func(*args, **kwargs)
        return decorated_admin
