import os.path

import sqlalchemy.exc
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from todo.user.forms import RegistrationForm, LoginForm, UpdateFormInfo, UpdatePass
from todo import bcrypt, db
from todo.models import User, Todo
from todo.user.utils import save_picture, random_avatar

users = Blueprint('users', __name__, template_folder='templates')

@users.route('/register', methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.main_page'))

    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data,email=form.email.data,password=hashed_password, image_file=random_avatar(form.username.data))
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались на нашем сайте!', 'success')
        login_user(user)

        return redirect(url_for('main.home_page'))

    return render_template('users/register.html', title='Регистрация', legend='Регистрация', form=form)

@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.password and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Вы вошли как пользователь {current_user.username}', 'info-msg')
            return redirect(next_page) if next_page else redirect(url_for('main.home_page'))
        else:
            flash('Войти не удалось. Пожалуйста, проверьте свой логин и пароль', 'danger')

    return render_template('users/login.html', form=form, title='Авторизация', legend='Войти')

@users.route('/account')
@login_required
def account():
    td = Todo.query.filter_by(creator=current_user).all()
    completed_td = db.session.query(Todo).filter_by(creator=current_user, status='Выполнено').all()
    active_td = db.session.query(Todo).filter_by(creator=current_user, status='Начато').all()
    return render_template('users/account.html', title='Аккаунт',completed_td=completed_td, todo=td, active_td=active_td)

@users.route('/settings', methods=['GET','POST'])
@login_required
def settings():
    user = User.query.filter_by(username=current_user.username).first()
    form=UpdateFormInfo()
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    elif form.validate_on_submit():
        path_one = os.path.join(os.getcwd(), f'todo/static/profile_pics/{user.username}')
        path_two = os.path.join(os.getcwd(), f'todo/static/profile_pics/{form.username.data}')
        os.rename(path_one, path_two)
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)
        else:
            form.picture.data = current_user.image_file

        db.session.commit()
        flash('Ваш аккаунт был обновлен!', 'success')
        return redirect(url_for('users.account'))
    return render_template('users/settings.html', title='Изменить пароль', form=form)

@users.route('/change_pass', methods=['GET','POST'])
@login_required
def change_pass():
    user = User.query.filter_by(username=current_user.username).first()
    form = UpdatePass()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.old_password.data):
            user.password = bcrypt.generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Ваш пароль был обновлен!','success')
            return redirect(url_for('users.account'))
    return render_template('users/change_pass.html', title='Изменить пароль', form=form)




@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home_page'))

