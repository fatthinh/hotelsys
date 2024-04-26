import models


def load_rooms():
    query = models.RoomType.query
    return query.all()
