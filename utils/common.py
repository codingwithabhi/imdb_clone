import jwt
import json
import hashlib
from db import db
from db import UserDetails
from flask import Response
from config import get_config


app_config = get_config()


def render_error_response(message='Internal Server Error', code=404):
    response = {
        'status': False,
        'message': str(message),
        'data': dict()
    }
    return Response(json.dumps(response), status=code, content_type='application/json')


def render_success_response(data=None, message='Success', code=200):
    body = {
        'status': True,
        'message': str(message),
        'data': data
    }
    return Response(json.dumps(body), status=code, content_type='application/json')


def generate_token(email):
    encoded = jwt.encode({"email": email}, app_config.get('SECRET'), algorithm="HS256")
    return str(encoded)


def encrypt_password(password):
    salt = app_config.get('SALT')
    unicode_password = (salt + str(password) + salt).encode()
    encrypted_password = hashlib.md5(unicode_password)
    return encrypted_password.hexdigest()


def validate_token(token):
    token_data = jwt.decode(token, app_config.get('SECRET'), algorithm='HS256')
    return token_data


def check_user_access(user_data):
    admin = db.session.query(UserDetails).filter(UserDetails.email == user_data.get('email'),
                                                 UserDetails.user_type == 'Admin').first()
    return admin

