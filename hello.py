import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, equal_to, length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

DEBUG = bool(os.getenv('DEBUG', True))
PORT = int(os.getenv('PORT', 8080))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my hot pot secret key'

# Old SQLite DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/postgres'

#New MySql DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://erlit:karbaFosbiz1!@localhost/our_users'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    favorite_color = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    # Do some password stuff!
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    # Create a string
    def __repr__(self):
        return f'<Name {self.name}>'

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    favorite_color = StringField('Favorite Color')
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

# Create a Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())
    slug = db.Column(db.String(255))

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()], widget=TextArea())
    author = StringField('Author', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Post')

@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html', posts=posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Update Database
        db.session.add(post)
        db.session.commit()
        flash('Post has been updated')
        return redirect(url_for('post', id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form=form)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        # Add post to database
        db.session.add(post)
        db.session.commit()

        flash('Post submitted successfully')
    return render_template('add_post.html', form=form)

#JSON
@app.route('/date')
def get_current_date():
    favorite_pizza = {'Mary': 'Pepperoni', 'Mark': 'Cheese', 'Tim': 'Pineapple'}
    return favorite_pizza
    #return {'Date': date.today()}


# Get update DB
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash('User updated successfully')
            return render_template('update.html', form=form, name_to_update=name_to_update)
        except:
            flash('Something went wrong')
            return render_template('update.html', form=form, name_to_update=name_to_update)
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update, id=id)

@app.route('/user/add', methods = ['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
            user = Users(name=form.name.data, email=form.email.data,
                         favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        email = form.email.data
        favorite_color = form.favorite_color.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = '***.data'
        flash('User Added')
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)

@app.route('/delete/<int:id>')
def delete(id):
    name = None
    form = UserForm()
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User deleted successfully')
        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html', form=form, name=name, our_users=our_users)
    except:
        flash('Something went wrong')
        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html', form=form, name=name, our_users=our_users)

@app.route('/')
def index():
    first_name = 'Miha'
    stuff = 'This is <strong>bold</strong> text'
    favorite_pizza = ['pepperoni', 'mexicana', 'four cheese']
    return render_template('index.html', first_name=first_name,
                                         stuff=stuff,
                                         favorite_pizza=favorite_pizza)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)

@app.route('/test_pw', methods = ['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''
        # Lookup USer by Email
        pw_to_check = Users.query.filter_by(email=email).first()
        # Check Hashed Password
        passed = check_password_hash(pw_to_check.password_hash, password)
    return render_template('test_pw.html', email=email, password=password,
                           form=form, pw_to_check=pw_to_check, passed=passed)

@app.route('/name', methods = ['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Success')
    return render_template('name.html', name=name, form=form)

#Bad Request - 500
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
#Invalid URL - 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)

# Create SQLite DB from terminal
# from hello import app, db
# app.app_context().push()
# db.create_all()

# Terminal commands
# FLASK_APP=app.py
# FLASK_DEBUG=1
# TEMPLATES_AUTO_RELOAD=1
# flask run

# open mysql
# mysql -u root -p

# Create MySQL DB from terminal
# pip install pymysql
# pip install criptography
# python create_db.py
# Create MySQL DB from terminal
# from hello import app, db
# app.app_context().push()
# db.create_all()

# Make migrations
# $pip install Flask-Migrate
# $FLASK_APP=hello.py flask db init
# from flask_migrate import Migrate
# migrate = Migrate(app, db)
# $FLASK_APP=hello.py flask db migrate -m 'First'
# $FLASK_APP=hello.py flask db upgrade

#PostgeSQL
# Login with root ubuntu password
#$ sudo -i -u postgres

# create a new role and pass
#$ sudo -i -u postgres
#psql
#CREATE ROLE XXX WITH LOGIN ENCRYPTED PASSWORD 'YYYYY';

# create a password for user
#$ sudo -i -u postgres
#psql
#\password postgres

#Acces with a user and password
#psql -U postgres -W

# Note that you can connect to a specific database when you log in to the PostgreSQL database server:
#
# $ psql -U postgres -d dvdrental
# In this command, the -d flag means database. In this command, you connect to t
# he dvdrental database using the postgres user.


#Переключиться на другую БД:
#$ psql -d postgres

#How to create a new table with SQLAlchemy
# Enter a python command line - $python
# from hello import db, app
# app.app_context().push()
# db.create_all()

# How to migrate
# $FLASK_APP=hello.py flask db init
# $FLASK_APP=hello.py flask db migrate -m 'First'
# $FLASK_APP=hello.py flask db upgrade

