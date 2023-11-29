from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Optional, Length, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('¿Recordar?')
    submit = SubmitField('Iniciar sesion')

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Repetir Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Crear usuario')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Use otro nombre de usuario')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Use otro correo')

class DatosForm(FlaskForm):
    texto = TextAreaField('Texto', validators=[Optional(), Length(max=200)])
    boolean = BooleanField('Booleano', validators=[DataRequired()])
    submit = SubmitField('Enviar datos')