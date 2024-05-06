from datetime import datetime


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


def room_serializer(room):
    return {
        "id": room.id,
        "name": room.name,
        "room_type": room.room_type
    }
