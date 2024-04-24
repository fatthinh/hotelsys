from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from __init__ import app, db

admin = Admin(app, name="Admin", template_mode="bootstrap4")
