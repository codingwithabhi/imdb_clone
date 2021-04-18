from db import db
from db import MovieDetails


def check_movie_exist(movie_name):
    movie = db.session.query(MovieDetails).filter(MovieDetails.name == movie_name).first()
    return movie


def add_movie(post_data, user_data):
    post_data['genre'] = str(post_data['genre'])
    post_data['added_by'] = user_data.get('email')
    movie_details_obj = MovieDetails(**post_data)
    db.session.add(movie_details_obj)
    db.session.commit()


def delete_movie(post_data):
    db.session.query(MovieDetails).filter(MovieDetails.name == post_data.get('name')).delete()
    db.session.commit()


def update_movie(post_data, user_data, movie_obj):
    if post_data.get('genre'):
        post_data['genre'] = str(post_data['genre'])
    post_data['edited_by'] = user_data.get('email')

    if "new_name" in post_data.keys():
        post_data['name'] = post_data.get('new_name')
        post_data.pop('new_name')

    db.session.query(MovieDetails).filter(MovieDetails.id == movie_obj.id).update(post_data)
    db.session.commit()


def search_movies(post_data):
    movies_obj = db.session.query(MovieDetails)
    if "name" in post_data.keys():
        name = f"%{post_data.get('name')}%"
        movies_obj = movies_obj.filter(MovieDetails.name.like(name))
    if "director" in post_data.keys():
        director = f"%{post_data.get('director')}%"
        movies_obj = movies_obj.filter(MovieDetails.director.like(director))
    if "genre" in post_data.keys():
        for genre in post_data.get('genre'):
            genre = f"%{genre}%"
            movies_obj = movies_obj.filter(MovieDetails.genre.like(genre))

    data_list = [movie.to_json() for movie in movies_obj]
    return data_list
