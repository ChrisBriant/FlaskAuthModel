from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp
from app.models.account import Account
from app.extensions import db
from .forms import *
import bcrypt


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{10,}$',message='Password does not meet complexity requirements.')])
    confirmpass = PasswordField('Confirm Password')

    def validate(self):
        result = super().validate()
        if not result:
            return False

        if self.password.data != self.confirmpass.data:
            print(self.password.errors)
            self.password.errors += ('Passwords do not match.',)
            return False

        return True

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate(self):
        result = super().validate()
        if not result:
            return False

        #Validate the account
        #Check account password matches hash - DONE
        #Check account exists - DONE
        #Check account is enabled
        account_found = Account.query.filter_by(email=self.email.data).first()
        if not account_found:
            self.email.errors += ('Sorry an account with this email address has not been found.',)
            return False

        if not account_found.is_enabled:
            self.email.errors += ('Your account is locked out.',)
            return False

        print('Found Account', self.password.data, account_found.password)
        if not bcrypt.checkpw(bytes(self.password.data,'UTF-8'), bytes(account_found.password,'UTF-8')):
            self.password.errors += ('Password is incorrect.',)
            return False

        return True