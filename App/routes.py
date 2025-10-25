import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from .models import User, Book, Cart, Order, OrderBook
from .forms import LoginForm, RegisterForm, AccountForm, BookForm, UpdateBookForm
from . import db, bcrypt
from flask_mail import Message
from App import mail

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    books = Book.query.limit(6).all()
    return render_template('home.html', books=books)

@bp.route('/books')
@login_required
def books():
    books = Book.query.all()
    carts = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template('books.html', books=books, carts=carts)


@bp.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()  

        
        msg = Message(
            'Welcome to BookStore! 🎉',    # Send welcome email
            recipients=[form.email.data]
            )
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f7;
            margin: 0;
            padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 30px auto;
                background-color: #ffffff;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    padding-bottom: 20px;
                    border-bottom: 1px solid #eaeaea;
                    }}
                .header h1 {{
                    color: #333333;
                    }}
                .content {{
                    padding: 20px 0;
                    color: #555555;
                    line-height: 1.6;
                    }}
                .button {{
                    display: inline-block;
                    padding: 12px 25px;
                    margin-top: 20px;
                    background-color: #1d72b8;
                    color: white !important;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                        }}
                .footer {{
                    margin-top: 30px;
                    font-size: 12px;
                    color: #999999;
                    text-align: center;
                        }}
        </style>
        </head>
        <body>
            <div class="container">
            <div class="header">
                <h1>Welcome to BookStore, {form.username.data}!</h1>
            </div>
            <div class="content">
                <p>Hi {form.username.data},</p>
                <p>We’re thrilled to have you at <strong>BookStore</strong>! 📚</p>
                <p>Explore our vast collection of books and start your reading journey today.</p>
                <p>Click the button below to start browsing:</p>
                <a href="http://127.0.0.1:5000/" class="button">Browse Books</a>
            </div>
            <div class="footer">
                <p>– BookStore Team</p>
                <p>If you did not create this account, please ignore this email.</p>
            </div>
            </div>
            </body>
            </html>
            """
        mail.send(msg)  # send the email
        
        flash('Account created. Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Check credentials.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('main.home'))


@bp.route('/account', methods=['GET', 'POST']) #  User Account 
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.state = form.state.data
        current_user.pincode = form.pincode.data
        if form.picture.data:
            filename = secure_filename(form.picture.data.filename)
            path = os.path.join(current_app.root_path, '..', 'static', 'Profile_Image', filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            form.picture.data.save(path)
            current_user.image_file = filename
        db.session.commit()
        flash('Account updated.', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.state.data = current_user.state
        form.pincode.data = current_user.pincode
    image_file = url_for('static', filename='Profile_Image/' + current_user.image_file)
    return render_template('account.html', form=form, image_file=image_file)


@bp.route('/addcart/<int:book_id>', methods=['POST']) #  Cart 
@login_required
def addcart(book_id):
    book = Book.query.get_or_404(book_id)
    if book.piece <= 0:
        flash('Out of stock', 'warning')
        return redirect(url_for('main.books'))
    cart_item = Cart.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    existing = Cart.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if existing:
        existing.quantity += 1
    else:
        cart_item = Cart(user_id=current_user.id, book_id=book_id, quantity=1)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Cart updated', 'success')
    return redirect(request.referrer or url_for('main.books'))


@bp.route('/cart')
@login_required
def cart():
    carts = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(item.cartbook.price * item.quantity for item in carts)
    return render_template('cart.html', carts=carts, total=total)


@bp.route('/delete_cart/<int:cart_id>', methods=['POST'])
@login_required
def delete_cart(cart_id):
    item = Cart.query.get_or_404(cart_id)
    db.session.delete(item)
    db.session.commit()

    # Recalculate total
    carts = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(i.cartbook.price * i.quantity for i in carts)

    return jsonify({
        'success': True,
        'message': 'Item removed from cart',
        'total': total
    })





@bp.route('/cart_update/<int:book_id>', methods=['POST'])
@login_required
def cart_update(book_id):
    data = request.get_json()
    action = data.get('action')
    cart_item = Cart.query.filter_by(user_id=current_user.id, book_id=book_id).first()

    if not cart_item and action == 'add':
        cart_item = Cart(user_id=current_user.id, book_id=book_id, quantity=1)
        db.session.add(cart_item)
    elif cart_item:
        if action == 'add':
            cart_item.quantity += 1
        elif action == 'remove':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                db.session.delete(cart_item)

    db.session.commit()
    return jsonify({
        'success': True,
        'quantity': cart_item.quantity if cart_item else 0
    })


@bp.route('/checkout', methods=['GET', 'POST'])  # Checkout & Orders
@login_required
def checkout():
    carts = Cart.query.filter_by(user_id=current_user.id).all()
    if not current_user.address:
        flash('Add address in your account before checkout', 'warning')
        return redirect(url_for('main.account'))

    total = sum(item.cartbook.price * item.quantity for item in carts)

    if request.method == 'POST':
        # Simulate payment success
        data = request.get_json()
        if data.get('payment') == 'success':
            return jsonify({'success': True, 'redirect': url_for('main.confirm_order')})
        return jsonify({'success': False, 'message': 'Payment failed!'})

    return render_template('checkout.html', carts=carts, total=total)

@bp.route('/confirm_order')
@login_required
def confirm_order():
    carts = Cart.query.filter_by(user_id=current_user.id).all()
    if not carts:
        flash('Cart is empty', 'warning')
        return redirect(url_for('main.cart'))

    total = sum(item.cartbook.price * item.quantity for item in carts)
    order = Order(user_id=current_user.id, amount=total, status="Pending")
    db.session.add(order)
    db.session.commit()

   
    for item in carts:   # Add books to order and update stock
        ob = OrderBook(order_id=order.id, book_id=item.book_id, quantity=item.quantity)
        book = Book.query.get(item.book_id)
        if book:
            book.piece = max(0, book.piece - item.quantity)
        db.session.add(ob)
        db.session.delete(item)
    db.session.commit()

    
    msg = Message(      # Send HTML email
        f'Order Confirmation #{order.id} - BookStore',
        recipients=[current_user.email]
    )

    order_rows = ''.join([f"<tr><td>{ob.book.title}</td><td>{ob.quantity}</td><td>₹{ob.book.price}</td></tr>" for ob in order.items])
    
    msg.html = f"""
    <h2>Thank you for your order, {current_user.username}!</h2>
    <p>Your order #{order.id} has been successfully placed.</p>
    <p><strong>Total Amount:</strong> ₹{total}</p>
    <h4>Order Details:</h4>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr><th>Book</th><th>Quantity</th><th>Price</th></tr>
        {order_rows}
    </table>
    <p>We will notify you when your books are shipped.</p>
    <p>- BookStore Team 📚</p>
    """
    mail.send(msg)

    flash('Order placed successfully! Confirmation email sent.', 'success')
    return redirect(url_for('main.orders'))

@bp.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).all()
    return render_template('orders.html', orders=user_orders)

@bp.route('/order/<int:order_id>')
@login_required
def detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash("Access denied", "danger")
        return redirect(url_for("main.orders"))
    orderbooks = OrderBook.query.filter_by(order_id=order.id).all()
    total = sum(ob.book.price * ob.quantity for ob in orderbooks)
    return render_template('invoice.html', order=order, orderbooks=orderbooks, total=total)

 
@bp.route('/search_books')   # Book Search
def search_books():
    query = request.args.get("q", "").strip()
    if query:
        books = Book.query.filter(Book.title.ilike(f"%{query}%")).all()
    else:
        books = Book.query.all()
    return render_template('book_card_list.html', books=books, carts=current_user.carts if current_user.is_authenticated else [])
