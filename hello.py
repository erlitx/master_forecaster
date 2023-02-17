import os
from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

DEBUG = bool(os.getenv('DEBUG', True))
PORT = int(os.getenv('PORT', 8080))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my hot pot secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    # Create a string
    def __repr__(self):
        return f'<Name {self.name}>'

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Push')

# Get update DB
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash('User updated successfully')
            return render_template('update.html', form=form, name_to_update=name_to_update)
        except:
            flash('Something went wrong')
            return render_template('update.html', form=form, name_to_update=name_to_update)
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update)

# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField('What is our name?', validators=[DataRequired()])
    submit = SubmitField('Push')

@app.route('/user/add', methods = ['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        email = form.email.data
        form.name.data = ''
        form.email.data = ''
        flash('User Added')
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

# Create DB from terminal
# from hello import app, db
# app.app_context().push()
# db.create_all()

# Terminal commands
# FLASK_APP=app.py
# FLASK_DEBUG=1
# TEMPLATES_AUTO_RELOAD=1
# flask run