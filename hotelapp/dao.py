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


def auth_user(email, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return models.User.query.filter(models.User.email.__eq__(email.strip()),
                                    models.User.password.__eq__(password)).first()


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
