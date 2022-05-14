from ast import Pass
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email(message="E-mail inválido")])
    password = PasswordField('password', validators=[DataRequired(), Length(min=5, max=30, message="Senha inválida")])

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email(message="E-mail inválido")])
    password = PasswordField('password', validators=[DataRequired(), Length(min=5, max=30, message="Senha inválida")])

class LinkForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=0, max=25, message="Limite de 25 caracteres")])
    descricao = StringField('descricao', validators=[Length(min=0, max=60, message="Limite de 100 caracteres")])
    link = StringField('link', validators=[DataRequired()])
    public = BooleanField('public')

