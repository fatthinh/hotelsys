import models
import hashlib
from __init__ import db


def get_room_types():
    query = models.RoomType.query
    return query.all()


def get_room_type_by_id(id):
    return models.RoomType.query.get(id)


def get_user_by_id(id):
    return models.User.query.get(id)


def get_rooms():
    return models.Room.query.all()


def get_room_by_id(id):
    return models.Room.query.get(id)


def get_guests():
    return models.Guest.query.all()


def get_guest_by_id(id):
    return models.Guest.query.get(id)


def get_amenity_types():
    return models.AmenityType.query.all()


def auth_user(email, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return models.User.query.filter(models.User.email.__eq__(email.strip()),
                                    models.User.password.__eq__(password)).first()


def add_booking(booker, cart):
    if booker and cart:
        booking = models.Booking(
            name=booker['name'], phone=booker['phone'], email=booker['email'], notes=booker['notes'], check_out=cart['check_out'], check_in=cart['check_in'])
        db.session.add(booking)

        for guest_data in cart['guests']:
            room = guest_data['room']
            guest = [item for item in get_guests() if guest_data['identity']
                     == item.identity_num]

            if guest:
                guest = guest[0]
            else:
                guest = models.Guest(
                    name=guest_data['name'], identity_num=guest_data['identity'], is_vietnamese=guest_data['is_vietnamese'])
                db.session.add(guest)
                db.session.commit()

            booking_guest = models.BookingGuest(
                booking_id=booking.id, guest_id=guest.id, room_id=room)
            db.session.add(booking_guest)

        for room_data in cart['items']:
            room = get_room_by_id(room_data['room'])
            booking.add_room(room=room)

        db.session.commit()


def load_room_detail(room_id):
    # Truy vấn RoomType cùng với danh sách các Amenity có trong đó
    query = (
        db.session.query(models.RoomType, models.Amenity,
                         models.AmenityRoom.quantity)
        .join(models.AmenityRoom, models.RoomType.id == models.AmenityRoom.room)
        .join(models.Amenity, models.Amenity.id == models.AmenityRoom.amenity)
        .filter(models.RoomType.id == room_id)
        .all()
    )

    # Tạo một từ điển chứa thông tin RoomType và danh sách các Amenity
    room_type_info = {}
    for room_type, amenity, quantity in query:
        if 'room_type' not in room_type_info:
            # Lưu thông tin RoomType
            room_type_info['room_type'] = {
                'id': room_type.id,
                'name': room_type.name,
                'room_size': room_type.room_size,
                'description': room_type.description,
                'adults': room_type.adults,
                'children': room_type.children,
                'price': room_type.price
            }
            # Khởi tạo danh sách Amenities
            room_type_info['amenities'] = []
        # Thêm thông tin của mỗi Amenity vào danh sách Amenities
        room_type_info['amenities'].append({
            'id': amenity.id,
            'name': amenity.name,
            'description': amenity.description,
            'quantity': quantity
        })

    return room_type_info
