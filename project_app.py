from flask_cors import CORS
from config import get_config
from db import db
from flask import Flask
from flask_restful import Api, Resource
from user_module import views as user_view
from movie import views as movie_view


def create_app():
    new_app = Flask(__name__)
    CORS(new_app)
    new_app.config.update(get_config())
    db.init_app(new_app)
    with new_app.app_context():
        db.create_all()
    return new_app


def add_urls(app_init):
    start_api = Api(app_init, catch_all_404s=True)
    start_api.add_resource(user_view.UserOperations, '/v1/create_user', methods=['POST'], endpoint='CREATE_USER')
    start_api.add_resource(movie_view.MovieOperations, '/v1/add_movie', methods=['POST'], endpoint='ADD_MOVIES')
    start_api.add_resource(movie_view.MovieOperations, '/v1/remove_movie', methods=['DELETE'], endpoint='REMOVE_MOVIES')
    start_api.add_resource(movie_view.MovieOperations, '/v1/update_movie', methods=['PUT'], endpoint='UPDATE_MOVIES')
    start_api.add_resource(movie_view.MovieDetails, '/v1/movie_details', methods=['GET'], endpoint='GET_MOVIE_DETAILS')
    start_api.add_resource(movie_view.MovieSearch, '/v1/search_movies', methods=['GET'], endpoint='SEARCH_MOVIES')
    return start_api


def start_app():
    init_app = create_app()
    init_api = add_urls(init_app)
    return init_app, init_api


app, api = start_app()
