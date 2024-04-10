from __init__ import db, app
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, Boolean, DateTime, Enum, Double, Table, BINARY
from datetime import datetime
from sqlalchemy.orm import relationship
from enum import Enum as Enumeration
import json
import hashlib


class UserRole(Enumeration):
    ADMIN = 1
    CUSTOMER = 2
    EMPLOYEE = 3


class BookingStatus(Enumeration):
    PAID = 1
    DEPOSIT = 2


class Currency(Enumeration):
    DOLLAR = 1
    VND = 2


class Rating(Enumeration):
    BAD = 1
    NOT_BAD = 2
    GOOD = 3
    VERY_GOOD = 4
    EXCELLENT = 5


class PaymentMethod(Enumeration):
    BANKING = 1
    CASH = 2


class UserInfo(db.Model):
    __abstract__ = True
    id = Column(Integer, autoincrement=True, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50), nullable=False)
    dob = Column(Date)

    def __str__(self):
        return self.last_name


class User(UserInfo):
    phone = Column(String(10), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    address = Column(String(255))
    avatar = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    active = Column(Boolean, default=True)


class Customer(UserInfo):
    vietnamese = Column(Boolean, default=True)

    def __str__(self):
        return self.vietnamese


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class Branch(Base):
    about = Column(String(255))
    address = Column(String(255), unique=True, nullable=False)
    hotline = Column(String(12), nullable=False)
    email = Column(String(50), nullable=False)
    services = relationship('Service', backref='branches',
                            secondary='branch_service')
    policies = relationship('Policy', backref='branches',
                            secondary='branch_policy')
    rooms = relationship('Room', backref='branch', lazy=True)


class Service(Base):
    description = Column(String(255))
    price = Column(Double, nullable=False)
    unit = Column(String(10), nullable=False)


branch_service = Table('branch_service',
                       Base.metadata,
                       Column('branch_id', Integer, ForeignKey(
                           Branch.id), primary_key=True),
                       Column('service_id', Integer, ForeignKey(Service.id), primary_key=True))


class Policy(Base):
    description = Column(String(255))


branch_policy = Table('branch_policy',
                      Base.metadata,
                      Column('branch_id', Integer, ForeignKey(
                          Branch.id), primary_key=True),
                      Column('policy_id', Integer, ForeignKey(Policy.id), primary_key=True))


class AmenityType(Base):
    amenities = relationship('Amenity', backref="type", lazy=True)


class Amenity(Base):
    quantity = Column(Integer, default=1)
    amenity_type = Column(Integer, ForeignKey(AmenityType.id))


class RoomType(Base):
    price = Column(Double, nullable=False)
    room_size = Column(Float)
    description = Column(String(255))
    adults = Column(Integer, default=2)
    children = Column(Integer, default=1)
    amenities = relationship(
        'Amenity', secondary='room_amenity', lazy=True, backref='rooms')


class Room(Base):
    booked = Column(Boolean, default=False)
    branch = Column(Integer, ForeignKey(Branch.id))
    room_type = Column(Integer, ForeignKey(RoomType.id), nullable=False)


room_amenity = Table('room_amenity',
                     Base.metadata,
                     Column('room_id', Integer, ForeignKey(
                         RoomType.id), primary_key=True),
                     Column('amenity_id', Integer, ForeignKey(Amenity.id), primary_key=True))


class ClientBase(db.Model):
    __abstract__ = True
    id = Column(Integer, autoincrement=True, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())


class BookingForm(ClientBase):
    status = Column(Enum(BookingStatus), default=BookingStatus.DEPOSIT)
    booker = Column(Integer, ForeignKey(User.id), nullable=False)
    notes = Column(String(50))
    rooms = relationship(Room, secondary='room_reservation',
                         backref='reservations')
    customers = relationship(
        Customer, secondary='reservation_customer', backref='reservations')


class FrontDesk(db.Model):
    id = Column(Integer, ForeignKey(BookingForm.id), primary_key=True)
    bookerName = Column(String(100), nullable=False)
    cashier = Column(Integer, ForeignKey(User.id), nullable=False)
    phone = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)


booking_room = Table('booking_room',
                     ClientBase.metadata,
                     Column('room_id', Integer, ForeignKey(
                         Room.id), primary_key=True),
                     Column('booking_id', Integer,
                            ForeignKey(BookingForm.id), primary_key=True),
                     Column('check_in', Date, nullable=False),
                     Column('check_out', Date, nullable=False))

booking_customer = Table('booking_customer',
                         ClientBase.metadata,
                         Column('booking_id', Integer,
                                ForeignKey(BookingForm.id), primary_key=True),
                         Column('customer_id', Integer, ForeignKey(
                             Customer.id), primary_key=True))


class Invoice(ClientBase):
    amount = Column(Double, nullable=False)
    currency = Column(Enum(Currency), default=Currency.VND)
    reservation = Column(Integer, ForeignKey(BookingForm.id), nullable=False)
    method = Column(Enum(PaymentMethod), default=PaymentMethod.CASH)


class Review(ClientBase):
    content = Column(String(255))
    rating = Column(Enum(Rating), nullable=False)
    booking = Column(Integer, ForeignKey(BookingForm.id), nullable=False)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
