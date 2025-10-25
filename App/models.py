from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    image_file = db.Column(db.String(200), nullable=False, default='default.jpg')
    address = db.Column(db.String(200))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)

    carts = db.relationship('Cart', backref='user', lazy=True)
    orders = db.relationship('Order', backref='buyer', lazy=True, cascade="all, delete-orphan")


    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def set_password_raw_hash(self, hashed_pw):
        """Use this if you already have a hashed password string."""
        self.password = hashed_pw

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def __repr__(self):
        return f"<User {self.username}>"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    publication = db.Column(db.String(120))
    publication_date = db.Column(db.Date)  
    language = db.Column(db.String(50))    
    reading_age = db.Column(db.String(50))
    ISBN = db.Column(db.String(50))
    content = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False, default=0.0)
    piece = db.Column(db.Integer, nullable=False, default=0)
    image_file = db.Column(db.String(200), nullable=False, default='default_book.jpg')

    carts = db.relationship('Cart', backref='cartbook', lazy=True)
    orderbooks = db.relationship('OrderBook', backref='book', lazy=True)

    def __repr__(self):
        return f"<Book {self.title}>"

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    items = db.relationship('OrderBook', backref='order', lazy=True, cascade="all, delete")

class OrderBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
