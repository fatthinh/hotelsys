from __init__ import app
from flask import render_template
from admin import admin


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/booking')
def booking():
    return render_template('booking.html')


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
