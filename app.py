from flask import Flask, redirect, request, render_template, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from wtform_fields import *
from models import *

import psycopg2

# configure app
app = Flask(__name__)
app.secret_key='SECRET'

# configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://owurcgitodrdfe:818a61e3d62540b65687496432080bde91d90fd45cb1b9b31091a3a63c734b8d@ec2-3-219-229-143.compute-1.amazonaws.com:5432/dcn6b8vj3u3l1t'
db = SQLAlchemy(app)

# configure login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
def index():
  reg_form = RegistrationForm()

  # update database if validation success
  if reg_form.validate_on_submit():
    username = reg_form.username.data
    password = reg_form.password.data

    # hash password
    hashed_password = pbkdf2_sha256.hash(password)
    
    # add user to db
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    flash('Registration was successful. Please login to continue.', 'success')
    # re-route to login
    return redirect(url_for('login'))
  return render_template('index.html', form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
  login_form = LoginForm()

  if login_form.validate_on_submit():
    user_object = User.query.filter_by(username=login_form.username.data).first()
    login_user(user_object)
    return redirect(url_for('chat'))
  return render_template('login.html', form=login_form)


@app.route('/logout', methods=['GET'])
def logout():
  logout_user()
  flash('Logged out successfully.', 'success')
  return redirect(url_for('login'))


@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
  if not current_user.is_authenticated:
    flash('Please login.', 'danger')
    return redirect(url_for('login'))

  return 'chat with me'


if __name__ == '__main__':
  app.run(debug=True)
