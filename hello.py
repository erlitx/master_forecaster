import os
from flask import Flask, render_template, request

DEBUG = bool(os.getenv('DEBUG', True))
PORT = int(os.getenv('PORT', 8080))

app = Flask(__name__)

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

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)


