from __init__ import app, login_manager
from flask import render_template, request, session, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user
from admin import admin
import dao
import utils
from decorators import loggedin
from datetime import datetime, timedelta


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/booking')
def booking():
    check_in = request.args.get('check-in', datetime.today().date().strftime(
        '%Y-%m-%d'))
    check_out = request.args.get(
        'check-out', (datetime.today().date() + timedelta(days=1)).strftime(
            '%Y-%m-%d'))
    rooms = dao.get_room_types()

    dates = {"check_in": check_in, "check_out": check_out}
    return render_template('booking.html', rooms=rooms, check_in=check_in, check_out=check_out, dates=dates)


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/login', methods=['get', 'post'])
@loggedin
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = dao.auth_user(email=email, password=password)
        if user:
            login_user(user)
            next = request.args.get('next')
            return redirect(next if next else '/')

    return render_template('login.html')


@app.route('/logout', methods=['get'])
def logout():
    logout_user()
    return redirect('/login')


@app.route('/api/rooms', methods=['get'])
def get_rooms():
    rooms = dao.get_room_types()
    return {'data': [utils.room_type_serializer(room) for room in rooms]}


@app.route('/api/cart', methods=['get'])
def get_cart():
    cart = session.get('cart')
    if not cart:
        return jsonify({})

    return jsonify(utils.get_cart_total(cart))


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get('id'))

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            'id': id,
            'quantity': 1,
        }

    session['cart'] = cart

    return jsonify(utils.get_cart_total(cart))


@app.route('/api/cart/<room_id>', methods=['delete'])
def delete_cart_item(room_id):
    cart = session.get('cart')
    if cart and room_id in cart:
        del cart[room_id]
        session['cart'] = cart

    return jsonify(utils.get_cart_total(cart))


@app.route('/api/cart/<room_id>', methods=['put'])
def update_cart_item(room_id):
    cart = session.get('cart')
    if cart and room_id in cart:
        quantity = int(request.json.get("quantity", 0))
        if (quantity == 0):
            cart[room_id]['quantity'] = 1
        else:
            cart[room_id]['quantity'] = quantity

        session['cart'] = cart

    return jsonify(utils.get_cart_total(cart))


@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/room-detail/<room_id>', methods=['get'])
def room_detail(room_id):
    room = dao.load_room_detail(room_id)
    print(room)
    return render_template('room-detail.html', room=room)


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
