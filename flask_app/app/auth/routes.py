from flask import render_template, request, url_for, redirect
from app.auth import bp
from app.models.account import Account
from app.extensions import db
from flask_login import logout_user
from .forms import *
import bcrypt

@bp.route('/', methods=('GET', 'POST'))
def index():
    success_message = None
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            return redirect(url_for('authed_content.index'))
    return render_template('auth/index.html',form=form,success_message=success_message)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            #Send to the login form
            form = LoginForm()
            success_message = 'Thank you for registering. Please check your mailbox and follow the instructions to activate your account.'
            return redirect(url_for('auth.index',form=form,success_message=success_message))
            #return render_template('auth/index.html',form=form,success_message=success_message)
    return render_template('auth/register.html',form=form)


@bp.route('/verify/<code>', methods=('GET', 'POST'))
def verify(code):
    account_found = Account.query.filter_by(code=code).first()
    if account_found:
        account_found.is_enabled = True
        db.session.commit()
    return render_template('auth/verify.html', account_found=account_found)

@bp.route('/logout', methods=('GET', 'POST'))
@bp.route('/signout', methods=('GET', 'POST'))
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

@bp.route('/forgot', methods=('GET', 'POST'))
def forgot():
    success_message = None
    form = ForgotForm()
    if form.validate_on_submit():
        success_message = 'You have been sent a link to reset your password. Please visit your email and click on the link to complete the process.'
    return render_template('auth/forgotpassword.html',form=form,success_message=success_message)


@bp.route('/reset/<code>', methods=('GET', 'POST'))
def reset(code):
    error_message = None
    success_message = None
    form = ResetPasswordForm()
    if request.method == 'POST':
        #Check code exists
        account_found = Account.query.filter_by(code=code).first()
        if not account_found:
            error_message = 'Sorry, your account cannot be found, you can try resetting your password again.'
            return render_template('auth/resetpassword.html',form=form,error_message=error_message)
        if form.validate_on_submit():
            salt = bcrypt.gensalt()
            hashed_passwd = bcrypt.hashpw(bytes(form.password.data,'UTF-8'), salt)
            account_found.password = hashed_passwd
            db.session.commit()
            success_message = 'Your password has been reset successfully, you can login below.'
            form = LoginForm()
            return redirect(url_for('auth.index',form=form,success_message=success_message))
    return render_template('auth/resetpassword.html',form=form,error_message=error_message)
