from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
from datetime import timedelta

# App Config
app = Flask(__name__)
app.config['SECRET_KEY'] = '878436c0a462c4145fa59eec2c43a66a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {'users':'sqlite:///users.db','vehicalregistered':'sqlite:///vehicalregistered.db'}
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=120)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
safe_seralizer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Login Manager
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'user_login.login'
login_manager.login_message_category = 'info'

# Import Blueprint routes objects
from vms.user_login.routes import blue
from vms.users.routes import blue
from vms.admin.routes import blue

# Register Blueprint
app.register_blueprint(user_login.routes.blue,url_prefix='/')
app.register_blueprint(users.routes.blue,url_prefix='/')
app.register_blueprint(admin.routes.blue,url_prefix='/')