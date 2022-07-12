from flask import Flask, render_template
from templates.wtform_fields import *

import psycopg2


app = Flask(__name__)
app.secret_key = 'SECRET'


@app.route('/', methods=['GET', 'POST'])
def index():
  reg_form = RegistrationForm()
  if reg_form.validate_on_submit():
    return 'success!'

  return render_template('index.html', form = reg_form)


if __name__ == '__main__':
  app.run(debug=True)
