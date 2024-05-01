import dao
from flask import session
from datetime import datetime, timedelta


def string_to_date(str):
    return datetime.strptime(str, '%Y-%m-%d').date()


def room_type_serializer(room):
    return {
        "id": room.id,
        "name": room.name,
        "price": room.price,
        "room_size": room.room_size,
        "description": room.description,
        "adults": room.adults,
        "children": room.children
    }


def get_cart_total(cart):
    total_amount, total_quantity = 0, 0

    if cart:
        for item in cart.values():
            room = dao.get_room_type_by_id(item['id'])
            total_amount += item["quantity"] * room.price
            total_quantity += item["quantity"]

    return {
        'items': [item for item in session.get("cart").values()],
        'total_amount': total_amount,
        'total_quantity': total_quantity
    }


# def check_available(room_type, check_in, check_out):
#     check_in = string_to_date(check_in)
#     check_out = string_to_date(check_out)
#     rooms = []

#     for room in dao.get_rooms_by_type(room_type):
#         bookings = [booking for booking in room.bookings if booking.created_at >=
#                     datetime.now() - timedelta(days=30)]

#         available = True
#         for booking in bookings:
#             booking_in = booking.check_in
#             booking_out = booking.check_out
#             if not ((check_in < booking_in and check_out < booking_in) or check_in > booking_out):
#                 available = False
#         if available:
#             rooms.append(room)

#     return rooms
