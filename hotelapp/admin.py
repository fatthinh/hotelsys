from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from __init__ import app, db
from models import *

admin = Admin(app, name="Admin", template_mode="bootstrap4")
admin.add_view(ModelView(Account, db .session))
