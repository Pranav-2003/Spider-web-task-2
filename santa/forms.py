from flask_wtf import FlaskForm
from flask_login import current_user
from santa.models import User, Group, Members
from datetime import datetime
import datetime as dt
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    city = StringField('City', validators=[DataRequired(), Length(min=3)])
    state = StringField('State', validators=[DataRequired(), Length(min=3)])
    age = StringField('Age', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please enter a different one!')
        
class GroupForm(FlaskForm):
    name = StringField('Group name', validators=[DataRequired(), Length(min=2, max=20)])
    date = DateField('Date', validators=[DataRequired()])
    budget = StringField('Budget', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Create Group')
    
    def validate_date(self, date):
        if date.data < dt.date.today():
            raise ValidationError("The date cannot be in the past!")
        
class JoinForm(FlaskForm):
    searched = StringField("Enter a code to join Group", validators=[DataRequired()])
    submit = SubmitField("Join Group")
    
    def validate_searched(self, searched):
        grp = Group.query.filter_by(code=searched.data).first()
        if not grp:
            raise ValidationError("No such group exists!!!")
        else:
            m = Members.query.filter_by(gno=grp.sno,uid=current_user.id)
            if(m.count() !=0):
                raise ValidationError("You are already in the group!")
        
class UpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    city = StringField('City', validators=[DataRequired(), Length(min=3)])
    state = StringField('State', validators=[DataRequired(), Length(min=3)])
    age = StringField('Age', validators=[DataRequired()])
    submit = SubmitField('Update')
    
    
    
    
