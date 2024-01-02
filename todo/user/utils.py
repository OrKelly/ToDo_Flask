import os
import secrets
import random
import shutil

from flask import current_app, url_for
from flask_login import current_user
from PIL import Image


def save_picture(form_picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    full_path = os.path.join(current_app.root_path, 'static', 'profile_pics',
                             current_user.username)
    if not os.path.exists(full_path):
        os.mkdir(full_path)

    picture_path = os.path.join(full_path, picture_fn)
    output_size = (360, 360)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def random_avatar(user):
    full_path = os.path.join(os.getcwd(), 'todo/static', 'profile_pics', user)
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    full_path_avatar = os.path.join(os.getcwd(),'todo/static/profile_pics/Avatars')
    list_avatars = os.listdir(full_path_avatar)
    lst = random.choice(list_avatars)
    random_image_file = os.path.join(full_path_avatar, lst)
    shutil.copy(random_image_file, full_path)

    return lst
