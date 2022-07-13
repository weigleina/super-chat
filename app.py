from flask import Flask, render_template
from wtform_fields import *
from models import *
import psycopg2


app = Flask(__name__)
app.secret_key = 'SECRET'


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://owurcgitodrdfe:818a61e3d62540b65687496432080bde91d90fd45cb1b9b31091a3a63c734b8d@ec2-3-219-229-143.compute-1.amazonaws.com:5432/dcn6b8vj3u3l1t'
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
  reg_form = RegistrationForm()
  if reg_form.validate_on_submit():
    username = reg_form.username.data
    password = reg_form.password.data

    # check if username already exists
    user_object = User.query.filter_by(username=username).first()
    if user_object:
      return "Username already exists"

    # add user to db
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return "User created"

  return render_template('index.html', form = reg_form)


if __name__ == '__main__':
  app.run(debug=True)
