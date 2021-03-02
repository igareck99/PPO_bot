from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
app.config.from_object(Configuration)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)
from models import *
admin = Admin(app)
admin.add_view(ModelView(Pupil, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Sys_Admin, db.session))
admin.add_view(ModelView(Module, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(Group, db.session))
admin.add_view(ModelView(Solution, db.session))
admin.add_view(ModelView(Ticket, db.session))
admin.add_view(ModelView(Chat_table,db.session))
#sslify = SSLify(app)

token = 'https://api.telegram.org/bot1628527567:AAFoB0fsz-8QKfkGow8biMztfSDUuYWXSjw/'
stx = 'https://1417bc2834f7.ngrok.io'
s = 'https://api.telegram.org/bot1628527567:AAFoB0fsz-8QKfkGow8biMztfSDUuYWXSjw/setWebhook?url=' + 'https://1417bc2834f7.ngrok.io'
delete_d = 'https://api.telegram.org/bot1628527567:AAFoB0fsz-8QKfkGow8biMztfSDUuYWXSjw/deleteWebhook'

