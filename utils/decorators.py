from flask import request
from utils.common import render_error_response, validate_token
from jwt import ExpiredSignatureError, InvalidTokenError


def token_validator(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        try:
            token_data = validate_token(token)
            func.__self__.user_details = token_data
            return func(*args, **kwargs)
        except ExpiredSignatureError as e:
            return render_error_response(message="Token Expired", code=401)
        except InvalidTokenError as e:
            return render_error_response(message="Invalid Token", code=401)
        except Exception as e:
            print(e)
            return render_error_response(message="Error in Token", code=401)
    return wrapper
