from __init__ import db, app
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, Boolean, DateTime, Enum, Double, Table, BINARY, Text
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from enum import Enum as Enumeration
import json
import hashlib
from flask_login import UserMixin
from utils import string_to_date


class UserStatus(Enumeration):
    ACTIVE = 1
    BLACKLISTED = 2
    CANCELED = 3


class UserRole(Enumeration):
    ADMIN = 1
    CUSTOMER = 2
    RECEPTIONIST = 3


class RoomStatus(Enumeration):
    AVAILABLE = 1
    RESERVED = 2
    BEING_SERVICED = 3
    OTHER = 4


class Rating(Enumeration):
    POOR = 1
    FAIR = 2
    GOOD = 3
    VERY_GOOD = 4
    EXCELLENT = 5


class Person(db.Model):
    __abstract__ = True
    id = Column(Integer, autoincrement=True, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50), nullable=False)
    address = Column(Text)
    identity_num = Column(String(20), unique=True)


class User(Person, UserMixin):
    phone = Column(String(11), nullable=False, unique=True)
    email = Column(String(40), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    avatar = Column(String(100))
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)


class Guest(Person):
    is_vietnamese = Column(Boolean, default=True)


class ServiceStaff(Person):
    pass


class Amenity(db.Model):
    id = Column(Integer, autoincrement=True,  primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)


class RoomType(db.Model):
    id = Column(Integer, autoincrement=True,  primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    room_size = Column(Float, nullable=False)
    description = Column(Text)
    adults = Column(Integer, nullable=False,  default=2)
    children = Column(Integer, default=1)
    price = Column(Double, nullable=False)
    rooms = relationship("Room", lazy=True)

    def check_available(self, check_in, check_out):

        rooms = []

        if check_in and check_out:
            check_in = string_to_date(check_in)
            check_out = string_to_date(check_out)

            for room in self.rooms:
                bookings = [booking for booking in room.bookings if booking.created_at >=
                            datetime.now() - timedelta(days=30)]

                available = True
                for booking in bookings:
                    if not ((check_in < booking.check_in and check_out < booking.check_in) or check_in > booking.check_out):
                        available = False
                if available:
                    rooms.append(room)

        return rooms


class BaseAmenity(db.Model):
    __abstract__ = True
    id = Column(Integer, autoincrement=True,  primary_key=True)
    amenity = Column(Integer, ForeignKey(Amenity.id), nullable=False)
    quantity = Column(Integer, default=1)


class AmenityRoom(BaseAmenity):
    room = Column(Integer, ForeignKey(RoomType.id), nullable=False)


class Room(db.Model):
    id = Column(Integer, autoincrement=True,  primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    status = Column(Enum(RoomStatus), default=RoomStatus.AVAILABLE)
    room_type = Column(Integer, ForeignKey(RoomType.id), nullable=False)

    def check_available(self):
        return self.bookings


class Requirement (BaseAmenity):
    room = Column(Integer, ForeignKey(Room.id), nullable=False)
    reservation = Column(Integer, ForeignKey('reservation.id'), nullable=False)


class BaseForm(db.Model):
    __abstract__ = True
    id = Column(Integer, autoincrement=True,  primary_key=True)
    check_in = Column(Date, nullable=False, default=datetime.now)
    check_out = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Booking(BaseForm):
    first_name = Column(String(50))
    last_name = Column(String(50), nullable=False)
    phone = Column(String(11), nullable=False)
    email = Column(String(50), nullable=False)
    notes = Column(Text)
    receptionist = Column(Integer, ForeignKey(User.id))
    rooms = relationship(Room, secondary="booking_room", backref='bookings')
    guests = relationship(Guest, secondary="booking_guest", backref="bookings")


class Reservation(BaseForm):
    booking = Column(Integer, ForeignKey(Booking.id), unique=True)
    receptionist = Column(Integer, ForeignKey(User.id))
    rooms = relationship(Room, secondary="reservation_room",
                         backref='reservations')
    guests = relationship(
        Guest, secondary="reservation_guest", backref="reservations")


booking_room = Table("booking_room",
                     db.metadata,
                     Column('booking_id', Integer, ForeignKey(
                         Booking.id), primary_key=True),
                     Column('room_id', Integer, ForeignKey(Room.id), primary_key=True))


reservation_room = Table("reservation_room",
                         db.metadata,
                         Column('reservation_id', Integer, ForeignKey(
                             Reservation.id), primary_key=True),
                         Column('room_id', Integer, ForeignKey(Room.id), primary_key=True))

booking_guest = Table("booking_guest",
                      db.metadata,
                      Column('booking_id', Integer, ForeignKey(
                          Booking.id), primary_key=True),
                      Column('guest_id', Integer, ForeignKey(Guest.id), primary_key=True))

reservation_guest = Table("reservation_guest",
                          db.metadata,
                          Column('reservation_id', Integer, ForeignKey(
                              Reservation.id), primary_key=True),
                          Column('guest_id', Integer, ForeignKey(Guest.id), primary_key=True))


class Invoice(db.Model):
    __abstract__ = True
    receptionist = Column(Integer, ForeignKey(User.id))
    amount = Column(Double, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class BookingInvoice(db.Model):
    booking = Column(Integer, ForeignKey(Booking.id), primary_key=True)


class RevervationInvoice(db.Model):
    reservation = Column(Integer, ForeignKey(Reservation.id), primary_key=True)


class Policy(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))
    details = Column(Text)
    creator = Column(Integer, ForeignKey(User.id))


class Issue(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    room = Column(Integer, ForeignKey(Room.id), nullable=False)
    reservation = Column(Integer, ForeignKey(Reservation.id), nullable=False)
    policy = Column(Integer, ForeignKey(Policy.id))


class Review(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    reservation = Column(Integer, ForeignKey(Reservation.id), nullable=False)
    content = Column(Text)
    rating = Column(Enum(Rating), default=Rating.VERY_GOOD)
    created_at = Column(DateTime, default=datetime.now)


class Service(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))
    details = Column(Text)
    price = Column(Double, nullable=False)
    unit = Column(String(20))


class ReservationService(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    reservation = Column(Integer, ForeignKey(Reservation.id), nullable=False)
    service = Column(Integer, ForeignKey(Service.id), nullable=False)
    quantity = Column(Double, default=1)
    staff = Column(Integer, ForeignKey(ServiceStaff.id))


def clear_data(db):
    db.drop_all()
    db.session.commit()


def insert_data(db, obj, fileName):
    with open(f'data/{fileName}.json', encoding='utf-8') as f:
        items = json.load(f)
        for item in items:
            db.session.add(obj(**item))
    db.session.commit()


def insert_amenity_room():
    with open(f'data/amenity-room.json', encoding='utf-8') as f:
        items = json.load(f)
        for item in items:
            db.session.add(AmenityRoom(**item))
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        # db.create_all()

        # insert_data(db, Amenity, "amenity")
        # insert_data(db, RoomType, "roomType")

        # with open(f'data/users.json', encoding='utf-8') as f:
        #     items = json.load(f)
        #     for item in items:
        #         first_name = item['first_name']
        #         last_name = item['last_name']
        #         address = item['address']
        #         identity_num = item['identity_num']
        #         phone = item['phone']
        #         email = item['email']
        #         password = str(hashlib.md5(
        #             item['password'].encode('utf-8')).hexdigest())

        #         db.session.add(User(first_name=first_name, last_name=last_name, address=address,
        #                             identity_num=identity_num, phone=phone, email=email, password=password))
        #     db.session.commit()

        # insert_data(db, Room, "room")
        # insert_data(db, Guest, "guest")
        insert_data(db, Booking, "booking")
        insert_amenity_room()

        # clear_data(db)
