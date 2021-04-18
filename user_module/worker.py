from db import db
from db import UserDetails
from utils.common import generate_token, encrypt_password
from datetime import datetime


def check_user_exist(email):
    user_exist = db.session.query(UserDetails).filter(UserDetails.email == email).first()
    return user_exist


def add_new_user(post_data):
    token = generate_token(post_data.get('email'))
    post_data['token'] = token
    current_time = datetime.now()
    post_data['created_on'] = current_time
    post_data['updated_on'] = current_time
    safe_password = encrypt_password(post_data.get('password'))
    post_data['password'] = safe_password
    user_details_obj = UserDetails(**post_data)
    db.session.add(user_details_obj)
    db.session.commit()
    return token

