from flask import Flask, redirect, render_template, url_for
from wtform_fields import *
from models import *

import psycopg2


app = Flask(__name__)
app.secret_key = 'SECRET'


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://owurcgitodrdfe:818a61e3d62540b65687496432080bde91d90fd45cb1b9b31091a3a63c734b8d@ec2-3-219-229-143.compute-1.amazonaws.com:5432/dcn6b8vj3u3l1t'
db = SQLAlchemy(app)


@app.route('/', methods = ['GET', 'POST'])
def index():
  reg_form = RegistrationForm()

  # update database if validation success
  if reg_form.validate_on_submit():
    username = reg_form.username.data
    password = reg_form.password.data

    # hash password
    hashed_password = pbkdf2_sha256.hash(password)
    
    # add user to db
    user = User(username = username, password = hashed_password)
    db.session.add(user)
    db.session.commit()

    # re-route to login
    return redirect(url_for('login'))

  return render_template('index.html', form = reg_form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
  login_form = LoginForm()

  if login_form.validate_on_submit():
    return "Logged in"

  return render_template('login.html', form = login_form)

if __name__ == '__main__':
  app.run(debug = True)
