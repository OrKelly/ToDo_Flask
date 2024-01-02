import os.path

import sqlalchemy.exc
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from todo.todo.forms import CreateTodo
from todo import bcrypt, db
from todo.models import User, Todo

todos = Blueprint('todos', __name__, template_folder='templates')

@todos.route('/todo')
@login_required
def all_todo():
    active_td = db.session.query(Todo).filter_by(creator=current_user, status='Начато').all()
    return render_template('todos/all_todo.html', todos=active_td)

@todos.route('/todo/create', methods=['GET','POST'])
@login_required
def create_todo():
    form = CreateTodo()
    if form.validate_on_submit():
        td = Todo(name=form.name.data, body=form.body.data, creator=current_user)
        db.session.add(td)
        db.session.commit()
        flash('Вы успешно создали задачу!', 'success')
        return redirect(url_for('todos.all_todo'))

    return render_template('todos/create_todo.html', form=form, legend='Создать задачу')

@todos.route('/todo/<int:todo_id>')
@login_required
def todo(todo_id):
    td = Todo.query.filter_by(id=todo_id).first()
    return render_template('todos/todo.html', todo=td, title=td.name)

@todos.route('/todo/<int:todo_id>/delete')
@login_required
def delete_todo(todo_id):
    td = Todo.query.filter_by(id=todo_id).first()
    if current_user != td.creator:
        flash('Недостаточно прав для удаления!', 'danger')
        return redirect(url_for('todos.all_todo'))

    db.session.delete(td)
    db.session.commit()
    flash('Задача была успешно удалена!', 'success')

    return redirect(url_for('todos.all_todo'))


@todos.route('/todo/<int:todo_id>/complete')
@login_required
def complete_todo(todo_id):
    td = Todo.query.filter_by(id=todo_id).first()
    if current_user != td.creator:
        flash('Недостаточно прав!', 'danger')
        return redirect(url_for('todos.all_todo'))

    td.status = 'Выполнено'
    db.session.commit()
    flash('Задача была успешно завершена!', 'success')

    return redirect(url_for('todos.all_todo'))

@todos.route('/todo/<int:todo_id>/update', methods=['GET','POST'])
@login_required
def update_todo(todo_id):
    form = CreateTodo()
    td = Todo.query.filter_by(id=todo_id).first()
    if request.method == 'GET':
        form.name.data = td.name
        form.body.data = td.body

    if request.method == 'POST' and form.validate_on_submit():
        td.name = form.name.data
        td.body = form.body.data

        db.session.commit()
        flash('Задача было успешно обновлена!', 'success')
        return redirect(url_for('todos.all_todo'))

    return render_template('todos/update_todo.html', form=form, legend='Обновить задачу')

@todos.route('/todo/completed_todo')
@login_required
def completed_todo():
    completed_td = db.session.query(Todo).filter_by(creator=current_user, status='Выполнено').all()
    return render_template('todos/completed_todo.html', title='Выполненные задачи', todos=completed_td)


