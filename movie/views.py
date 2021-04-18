from flask import request
from flask_restful import Resource
from movie.schema import MovieSchema, MovieUpdateSchema, MovieDeleteSchema, MovieSearchSchema, MovieDetailsSchema
from marshmallow import ValidationError
from movie.worker import add_movie, check_movie_exist, delete_movie, update_movie, search_movies
from utils.decorators import token_validator
from utils.common import render_error_response, render_success_response, check_user_access


class AuthResource(Resource):
    def __init__(self):
        self.user_details = dict()

    method_decorators = [token_validator]


class MovieOperations(AuthResource):
    def __init__(self):
        super().__init__()
        self.get_data = request.args.to_dict()
        self.post_data = request.get_json()
        self.data = dict()

    def check_authorisation(self):
        is_admin = check_user_access(self.user_details)
        if not is_admin:
            return render_error_response(message="Permission Denied", code=403)

    def post(self):
        try:
            self.check_authorisation()
            try:
                MovieSchema().load(self.post_data)
            except ValidationError as e:
                return render_error_response(message=str(e), code=422)
            movie_exist = check_movie_exist(self.post_data.get('name'))
            if movie_exist:
                return render_error_response(message="Movie Already Exist!!!", code=409)
            add_movie(self.post_data, self.user_details)
        except Exception as e:
            print(e)
            return render_error_response()

        return render_success_response(data=self.data, message="Movie Added Successfully", code=201)

    def delete(self):
        try:
            self.check_authorisation()
            try:
                MovieDeleteSchema().load(self.post_data)
            except ValidationError as e:
                return render_error_response(message=str(e), code=422)
            movie_exist = check_movie_exist(self.post_data.get('name'))
            if not movie_exist:
                return render_error_response(message="Movie Does not Exist!!!", code=404)
            delete_movie(self.post_data)
        except Exception as e:
            print(e)
            return render_error_response()

        return render_success_response(data=self.data, message="Movie Removed Successfully", code=202)

    def put(self):
        try:
            self.check_authorisation()
            try:
                MovieUpdateSchema().load(self.post_data)
            except ValidationError as e:
                return render_error_response(message=str(e), code=422)
            movie_exist = check_movie_exist(self.post_data.get('name'))
            if not movie_exist:
                return render_error_response(message="Movie Does not Exist!!!", code=404)
            update_movie(self.post_data, self.user_details, movie_exist)
        except Exception as e:
            print(e)
            return render_error_response()

        return render_success_response(data=self.data, message="Movie Updated Successfully", code=202)


class MovieSearch(Resource):
    def __init__(self):
        self.get_data = request.args.to_dict()
        self.post_data = request.get_json()
        self.data = dict()

    def get(self):
        try:
            try:
                MovieSearchSchema().load(self.post_data)
            except ValidationError as e:
                return render_error_response(message=str(e), code=422)
            movies = search_movies(self.post_data)
            self.data = {"movies": movies}
        except Exception as e:
            print(e)
            return render_error_response()

        return render_success_response(data=self.data, message="Movie Listed Successfully", code=200)


class MovieDetails(Resource):
    def __init__(self):
        self.get_data = request.args.to_dict()
        self.post_data = request.get_json()
        self.data = dict()

    def get(self):
        try:
            try:
                MovieDetailsSchema().load(self.post_data)
            except ValidationError as e:
                return render_error_response(message=str(e), code=422)
            movie_exist = check_movie_exist(self.post_data.get('name'))
            if not movie_exist:
                return render_error_response(message="Movie Not Found !!!", code=404)
            movie_data = movie_exist.to_json()
            self.data = {"movie_details": movie_data}
        except Exception as e:
            print(e)
            return render_error_response()

        return render_success_response(data=self.data, message="Successful", code=200)



