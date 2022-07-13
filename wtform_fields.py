from ast import Eq
from configparser import LegacyInterpolation
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from models import *


def invalid_credentials(form, field):
  """ Verify username/password """

  username_entered = form.username.data
  password_entered = field.data

  user_object = User.query.filter_by(username=username.data).first()
  if user_object in None:
    raise ValidationError('Username or password is incorrect')
  # checks that stored hashed password is equal to user entered password
  elif not pbkdf2_sha256.verify(password_entered, user_object.password):
    raise ValidationError('Username or password is incorrect')


class RegistrationForm(FlaskForm):
  """ Registration Form """

  username = StringField('username', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
  password = PasswordField('password', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
  confirm_password = PasswordField('confirm_password', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])
  submit_button = SubmitField('Create')

  def validate_username(self, username):
    user_object = User.query.filter_by(username=username.data).first()
    if user_object:
      raise ValidationError('Username already exists')

class LoginForm(FlaskForm):
  """ Login form """

  username = StringField('username', validators=[InputRequired(message="Username required")])
  password = PasswordField('password', validators=[InputRequired(message="Password required"), invalid_credentials])
  submit_button = SubmitField('Login')