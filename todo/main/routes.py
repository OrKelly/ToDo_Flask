from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user

from todo.models import User, Todo

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def home_page():
    return render_template('main/main_page.html', title='Главная страница')