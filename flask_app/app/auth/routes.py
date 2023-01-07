from flask import render_template, request, url_for, redirect
from app.auth import bp
from app.models.account import Account
#from app.models.question import Question
from app.extensions import db
from .forms import *
import bcrypt

@bp.route('/', methods=('GET', 'POST'))
def index():
    form = LoginForm()
    if request.method == 'POST':
        print('I will check the login details here')
        if form.validate_on_submit():
            print('The form is valid')
            # print('The form is valid')
            # account_found = Account.query.filter_by(email=form.email.data).first()
            # print('Found Account', account_found.password)
            # print(bcrypt.checkpw(bytes(form.password.data,'UTF-8'), bytes(account_found.password,'UTF-8')))

    return render_template('auth/index.html',form=form)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        print('I will perform registration here')
        if form.validate_on_submit():
            salt = bcrypt.gensalt()
            hashed_passwd = bcrypt.hashpw(bytes(form.password.data,'UTF-8'), salt)
            account = Account(
                username= form.username.data,
                password = hashed_passwd,
                email = form.email.data,
                is_enabled = False
            )
            db.session.add(account)
            db.session.commit()
            print('Form is valid', hashed_passwd)
        else:
            print(form.errors)
        #return redirect(url_for('auth.index'))
    return render_template('auth/register.html',form=form)