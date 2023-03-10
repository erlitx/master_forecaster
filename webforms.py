from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, equal_to, length
#Reach text editor
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

# Search Form
class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    #content = StringField('Content', validators=[DataRequired()], widget=TextArea())
    content = CKEditorField('Body', validators=[DataRequired()])
    author = StringField('Author')
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Post')

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    favorite_color = StringField('Favorite Color')
    about_author = TextAreaField('About Author')
    profile_pic = FileField('Profile Pic')
    password_hash = PasswordField('Password', validators=[DataRequired(), equal_to('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Push')

# Password Class
class PasswordForm(FlaskForm):
    email = StringField('What is our email?', validators=[DataRequired()])
    password_hash = PasswordField('What is our password?', validators=[DataRequired()])
    submit = SubmitField('Push')

# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField('What is our name?', validators=[DataRequired()])
    submit = SubmitField('Push')

