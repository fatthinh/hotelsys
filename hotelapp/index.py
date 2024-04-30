from __init__ import app
from flask import render_template
from admin import admin
import dao


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/booking')
def booking():
    rooms = dao.load_rooms()
    print(rooms)
    return render_template('booking.html', rooms=rooms)


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/room-detail/<room_id>', methods=['get'])
def room_detail(room_id):
    room = dao.load_room_detail(room_id)

    print(room)

    return render_template('room-detail.html', room=room)


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
