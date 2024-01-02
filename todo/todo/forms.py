from datetime import datetime

from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField
from wtforms.fields import DateTimeField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, InputRequired
from wtforms.widgets import DateTimeInput


class CreateTodo(FlaskForm):
    name = StringField('Заголовок', validators=[DataRequired('Вы использовали неккоректные данные для заполнения заголовка!')])
    body = TextAreaField('Задача', validators=[DataRequired('Вы использовали неккоректные данные для заполнения задачи!')])
    #deadline = DateField('Выберите дату', format="%m/%d/%Y", validators=[DataRequired()])
    submit = SubmitField('Создать')
