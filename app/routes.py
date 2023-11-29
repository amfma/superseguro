from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, RegisterForm, DatosForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Contenido
from urllib import parse as url_parse
from app import db

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('content'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña invalido')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember.data)
        next = request.args.get('next')
        if not next or url_parse(next).netloc != '':
            next = url_for('index')
        return redirect('content')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('content'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('El usuario ha sido creado')
        return redirect(url_for('index'))
    return render_template('registrar.html', title='Registrar', form=form)

@app.route('/content', methods=['GET', 'POST'])
@login_required
def content():
    form = DatosForm()
    if form.validate_on_submit():
        content = Contenido(texto=form.texto.data, boolean=form.boolean.data)
        db.session.add(content)
        db.session.commit()
        flash('Los datos han sido agregados')
        return redirect(url_for('content'))
    return render_template('content.html', title='Contenido', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))