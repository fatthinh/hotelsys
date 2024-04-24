from __init__ import db, app
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, Boolean, DateTime, Enum, Double, Table, BINARY
from datetime import datetime
from sqlalchemy.orm import relationship
from enum import Enum as Enumeration
import json
import hashlib


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
