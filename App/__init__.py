import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="templates")
    app.config['SECRET_KEY'] = 'supersecretkey123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static')

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'group.bookbtore@gmail.com'
    app.config['MAIL_PASSWORD'] = 'oith blgb byry dhyq'  
    app.config['MAIL_DEFAULT_SENDER'] = 'group.bookbtore@gmail.com'

    
    db.init_app(app) # Initialize extensions
    mail.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    
    from .routes import bp as main_bp # Import blueprints
    from .admin_routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    return app

from .models import User, Book, Order, OrderBook, Cart

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
