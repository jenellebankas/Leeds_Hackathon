from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_admin import Admin
from flask_babel import Babel
from flask_login import LoginManager


def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')

app = Flask(name)
app.config.from_object('config')

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

babel = Babel(app, locale_selector=get_locale)
admin = Admin(app, template_mode='bootstrap4')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from app import views, models