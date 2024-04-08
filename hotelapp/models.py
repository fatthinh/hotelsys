from __init__ import db, app
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, Boolean, DateTime, Enum, Double, Table
from datetime import datetime
from sqlalchemy.orm import relationship, DeclarativeBase
from enum import Enum as Enumeration
import json
import hashlib
from sqlalchemy.ext.declarative import declarative_base


class UserRole(Enumeration):
    ADMIN = 'Admin'
    CUSTOMER = "Customer"
    EMPLOYEE = "Employee"


class ReservationStatus(Enumeration):
    PAID = "Paid"
    DEPOSIT = "Deposit"


class Currency(Enumeration):
    DOLLAR = 'Dollar'
    VND = "Đồng"


class Rating(Enumeration):
    BAD = 1
    NOT_BAD = 2
    GOOD = 3
    VERY_GOOD = 4
    EXCELLENT = 5


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


class Room(Base):
    booked = Column(Boolean, default=False)


class RoomType(Base):
    price = Column(Double, nullable=False)
    room_size = Column(Float)
    description = Column(String(255))
    adults = Column(Integer, default=2)
    children = Column(Integer, default=1)
    amenities = relationship(
        'Amenity', secondary='room_amenity', lazy=True, backref='rooms')


class AmenityType(Base):
    amenities = relationship('Amenity', backref="type", lazy=True)


class Amenity(Base):
    quantity = Column(Integer, default=1)
    amenity_type = Column(Integer, ForeignKey(AmenityType.id))


room_amenity = Table('room_amenity',
                     Base.metadata,
                     Column('room_id', Integer, ForeignKey(
                         Room.id), primary_key=True),
                     Column('amenity_id', Integer, ForeignKey(Amenity.id), primary_key=True))


class ClientBase(db.Model):
    __abstract__ = True
    id = Column(Integer, autoincrement=True, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())


class ReservationForm(ClientBase):
    status = Column(Enum(ReservationStatus), default=ReservationStatus.DEPOSIT)
    created_at = Column(DateTime, default=datetime.now())
    rooms = relationship(Room, secondary='room_reservation',
                         backref='reservations')
    customers = relationship(
        Customer, secondary='reservation_customer', backref='reservations')
    phone = Column(String(10), nullable=False)


class Booking(ReservationForm):
    booker = Column(Integer, ForeignKey(User.id), nullable=False)
    cashier = Column(Integer, ForeignKey(User.id), nullable=False)


room_reservation = Table('room_reservation',
                         ClientBase.metadata,
                         Column('room_id', Integer, ForeignKey(
                             Room.id), primary_key=True),
                         Column('reservation_id', Integer,
                                ForeignKey(ReservationForm.id), primary_key=True),
                         Column('checkIn', Date, nullable=False),
                         Column('checkOut', Date, nullable=False))

reservation_customer = Table('reservation_customer',
                             ClientBase.metadata,

                             Column('reservation_id', Integer,
                                    ForeignKey(ReservationForm.id), primary_key=True),
                             Column('customer_id', Integer, ForeignKey(
                                 Customer.id), primary_key=True))


class Invoice(ClientBase):
    amount = Column(Double, nullable=False)
    currency = Column(Enum(Currency), default=Currency.VND)
    reservation = Column(Integer, ForeignKey(ReservationForm.id))


class Review(ClientBase):
    content = Column(String(255))
    rating = Column(Enum(Rating), nullable=False)
    booking = Column(Integer, ForeignKey(Booking.id), nullable=False)
    owner = Column(Integer, ForeignKey(Booking.booker), nullable=False)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # with open('data/accounts.json', encoding='utf-8') as f:
        #     accounts = json.load(f)
        #     for account in accounts:
        #         last_name = account['last_name']
        #         phone = account['phone']
        #         email = account['email']
        #         password = account['password']

        #         u = Account(last_name=last_name, phone=phone, email=email, password=str(
        #             hashlib.md5(password.encode('utf-8')).hexdigest()))
        #         session.add(u)
        # db.session.commit()
