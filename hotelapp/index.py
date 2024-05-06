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


@app.route('/book', methods=['post'])
def book():
    if request.method == "POST":
        booker = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "notes": request.form.get("notes"),
        }
        try:
            dao.add_booking(booker, session.get('cart'))
        except Exception as ex:
            print(ex)
            return jsonify({'status': 500})
        else:
            del session['cart']

    return render_template('index.html')


@app.route('/booking')
def booking():
    check_in = request.args.get('check-in', datetime.today().date().strftime(
        '%Y-%m-%d'))
    check_out = request.args.get(
        'check-out', (datetime.today().date() + timedelta(days=1)).strftime('%Y-%m-%d'))
    cart = session.get('cart')

    if cart:
        if check_in != cart['check_in'] or check_out != cart['check_out']:
            session.pop('cart', default=None)

    rooms = dao.get_room_types()
    return render_template('booking.html', rooms=rooms, check_in=check_in, check_out=check_out)


@app.route('/checkout')
def checkout():
    rooms = dao.get_rooms()
    room_types = dao.get_room_types()
    return render_template('checkout.html', rooms=rooms, room_types=room_types, guests=session.get("guests"))


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


@app.route('/api/room_types', methods=['get'])
def get_room_types():
    rooms = dao.get_room_types()
    return {'data': [utils.room_type_serializer(room) for room in rooms]}


@app.route('/api/rooms', methods=['get'])
def get_rooms():
    rooms = dao.get_rooms()
    return {'data': [utils.room_serializer(room) for room in rooms]}


@app.route('/api/cart', methods=['get'])
def get_cart():
    cart = session.get('cart')
    if not cart:
        return jsonify({})

    return jsonify(get_cart_total(cart))


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    cart = session.get('cart')
    if not cart:
        cart = {
            "check_in": request.json.get("checkIn"),
            "check_out": request.json.get("checkOut"),
            'items': []
        }

    id = str(request.json.get('id'))

    room_type = dao.get_room_type_by_id(id)
    rooms = room_type.check_available(cart['check_in'], cart['check_out'])

    # if any(item['id'] == id for item in cart['items']):
    #     [item.update({'quantity': item['quantity'] + 1})
    #      for item in cart['items']
    #      if item['id'] == id and
    #      item['quantity'] < len(room_type.check_available(cart['check_in'], cart['check_out']))]
    # else:
    #     cart['items'].append({"id": id, "quantity": 1, "rooms": rooms})

    index = 0
    while (index < len(rooms) and any(item['room'] == rooms[index].id for item in cart['items'])):
        index += 1

    if index < len(rooms):
        cart['items'].append(
            {"room": rooms[index].id, "room_type": room_type.id})

    print(cart)
    session['cart'] = cart

    return jsonify(get_cart_total(cart))


@app.route('/api/cart/<room_id>', methods=['delete'])
def delete_cart_item(room_id):
    cart = session.get('cart')

    if cart:
        cart['items'] = [item for item in cart['items']
                         if item['room'] != int(room_id)]
        session['cart'] = cart

    return jsonify(get_cart_total(cart))


@app.route('/api/cart/<room_id>', methods=['put'])
def update_cart_item(room_id):
    cart = session.get('cart')
    if cart:
        quantity = int(request.json.get("quantity", 0))
        if (quantity == 0):
            [item.update({'quantity': 1})
             for item in cart['items'] if item['id'] == room_id]
        else:
            room = dao.get_room_type_by_id(room_id)
            [item.update({'quantity': quantity})
             for item in cart['items'] if item['id'] == room_id and
             quantity <= len(room.check_available(cart['check_in'], cart['check_out']))]

        session['cart'] = cart

    return jsonify(get_cart_total(cart))


def get_cart_total(cart):
    total_amount = 0

    if cart:
        for item in cart['items']:
            room_type = dao.get_room_type_by_id(item['room_type'])
            total_amount += room_type.price

    return {
        'items': cart['items'],
        'total_amount': total_amount,
        'total_quantity': len(cart['items']),
    }


@app.route('/api/guests', methods=['post'])
def add_guest_info():
    cart = session.get('cart')
    guests = cart.get('guests')
    if not guests:
        guests = []

    name = str(request.json.get('name'))
    identity = str(request.json.get('identity'))
    room = str(request.json.get("room_id"))
    is_vietnamese = request.json.get("is_vietnamese")

    if any(item['identity'] == identity for item in guests):
        [item.update({'name': name, 'room': room, "is_vietnamese": is_vietnamese})
         for item in guests
         if item['identity'] == identity]
    else:
        guests.append({"name": name, "identity": identity,
                      "room": room, "is_vietnamese": is_vietnamese})

    cart['guests'] = guests
    session['cart'] = cart

    print(session['cart'])

    return jsonify({})


@app.route('/api/guests', methods=['get'])
def get_guests_info():
    cart = session.get('cart')
    guests = cart.get('guests')

    if guests:
        print(guests)
        return jsonify(guests)
    return jsonify({})


@app.route('/api/guests/<guest_id>', methods=['delete'])
def remove_guest_info(guest_id):
    cart = session.get('cart')
    guests = cart.get('guests')

    if guests:
        cart['guests'] = [item for item in guests if item['identity'] != guest_id]

    session['cart'] = cart
    return jsonify({})


@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/room-detail/<room_id>', methods=['get'])
def room_detail(room_id):
    room = dao.load_room_detail(room_id)
    return render_template('room-detail.html', room=room)


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
