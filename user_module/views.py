from flask_restful import Resource
from flask import request
from user_module.schema import NewUser
from marshmallow import ValidationError
from user_module.worker import add_new_user, check_user_exist
from utils.common import render_error_response, render_success_response


class UserOperations(Resource):
    def __init__(self):
        self.get_data = request.args.to_dict()
        self.post_data = request.get_json()
        self.data = dict()

    def post(self):
        try:
            try:
                NewUser().load(self.post_data)
            except ValidationError as e:
                return render_error_response(message=str(e), code=422)
            user_exist = check_user_exist(self.post_data.get('email'))
            if user_exist:
                return render_error_response(message="User Exist!!!", code=409)
            token = add_new_user(self.post_data)
            self.data['token'] = token
        except Exception as e:
            print(e)
            return render_error_response()

        return render_success_response(data=self.data, message="User Created Successfully", code=201)
