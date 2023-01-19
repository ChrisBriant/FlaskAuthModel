from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp
from flask_login import login_user
from app.models.account import Account
from app.extensions import db
from .forms import *
from app import Config
from app.messaging.email import send_confirm_email, send_password_reset_email 
from sqlalchemy.exc import IntegrityError
import bcrypt, random, string

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
            self.password.errors += ('Passwords do not match.',)
            return False

        #Try to create the account
        try:
            salt = bcrypt.gensalt()
            hashed_passwd = bcrypt.hashpw(bytes(self.password.data,'UTF-8'), salt)
            #Code for activation
            # initializing size of string
            N = 32
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
             
            account = Account(
                username= self.username.data,
                password = hashed_passwd,
                email = self.email.data,
                is_enabled = False,
                code = code
            )
            db.session.add(account)
            db.session.commit()
            #Send activation email
            activation_url = f'{Config.BASE_URL}/auth/verify/{code}'
            send_confirm_email(self.email.data,self.username.data,activation_url)
        except IntegrityError as ie:
            #Handle a duplicate user account
            self.email.errors += ('An account already exists for this email address.',)
            return False
        except Exception as e:
            self.email.errors += ('Sorry, an error occured creating the account.',)
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
        #Check account password matches hash
        #Check account exists
        #Check account is enabled
        account_found = Account.query.filter_by(email=self.email.data).first()
        if not account_found:
            self.email.errors += ('Sorry an account with this email address has not been found.',)
            return False

        if not account_found.is_enabled:
            self.email.errors += ('Your account is locked out.',)
            return False

        if not bcrypt.checkpw(bytes(self.password.data,'UTF-8'), bytes(account_found.password,'UTF-8')):
            self.password.errors += ('Password is incorrect.',)
            return False
        login_user(account_found,remember=True)

        return True

class ForgotForm(FlaskForm):
    email = EmailField('Email', validators=[Email()])

    def validate(self):
        result = super().validate()
        if not result:
            return False
        
        #Try to find account
        account_found = Account.query.filter_by(email=self.email.data).first()
        if not account_found:
            self.email.errors += ('Sorry an account with this email address has not been found.',)
            return False

        #Create the code to send for the password reset
        N = 32
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        account_found.code = code
        db.session.commit()
        #SEND EMAIL
        activation_url = f'{Config.BASE_URL}/auth/reset/{code}'
        send_password_reset_email(self.email.data,account_found.username,activation_url)
        return True

        

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{10,}$',message='Password does not meet complexity requirements.')])
    confirmpass = PasswordField('Confirm Password')

    def validate(self):
        result = super().validate()
        if not result:
            return False
        
        if self.password.data != self.confirmpass.data:
            self.password.errors += ('Passwords do not match.',)
            return False
        return True