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
    return f'{self.name}'



# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField('What is our name?', validators=[DataRequired()])
    submit = SubmitField('Push')

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


