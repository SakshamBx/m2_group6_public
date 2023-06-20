from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DateField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Optional
import app.lib.db_methods as db_methods

class RegistrationForm(FlaskForm):
    # inputs for registration form
    user_fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])
    user_email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up')
    
class LoginForm(FlaskForm):
    # inputs for login form
    user_email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class BookingForm(FlaskForm):
    # inputs for booking form
    booking_date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Book')
