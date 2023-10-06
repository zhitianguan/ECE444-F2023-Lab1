from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

def check_utoronto_substring(form, field):
    email = field.data
    if 'utoronto' not in email:
        raise validators.ValidationError('Email address must contain "utoronto".')

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))

    uoft_check_failed = False
    if session.get('email') is not None:
        uoft_check_failed = 'utoronto' not in session.get('email')
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), uoft_check_failed=uoft_check_failed)
