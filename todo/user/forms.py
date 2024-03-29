from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import file_allowed
from wtforms import StringField, BooleanField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, InputRequired
from todo.models import User

class LoginForm(FlaskForm):
    email = StringField('Почта:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Введите ваше имя:', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Почта:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    repl_password = PasswordField('Повторите пароль:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Войти')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash('Это имя уже занято. Пожалуйста, попробуйте другое', 'danger')
            raise ValidationError('This username is taken. Please try an another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash('Этот email уже занят. Пожалуйста, попробуйте другой', 'danger')
            raise ValidationError('This email is taken. Please try an another one')

class UpdateFormInfo(FlaskForm):
    username = StringField('Имя:', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Почта:', validators=[DataRequired(), Email()])
    picture = FileField('Аватарка (png,jpg)', validators=[file_allowed(['jpg', 'png'])])
    submit = SubmitField('Изменить')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                flash('Это имя уже занято. Пожалуйста, попробуйте другое', 'danger')
                raise ValidationError('This username is taken. Please try an another one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                flash('Этот email уже занят. Пожалуйста, попробуйте другой', 'danger')
                raise ValidationError('This email is taken. Please try an another one')

class UpdatePass(FlaskForm):
    old_password = PasswordField('Старый пароль:', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль:', validators=[DataRequired()])
    repl_password = PasswordField('Повторите пароль:', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Изменить')