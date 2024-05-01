import models
import hashlib


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
