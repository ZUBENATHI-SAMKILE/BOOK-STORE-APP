from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Order, OrderBook, User, Book
from .forms import BookForm, UpdateBookForm
from . import db
import os


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.before_request
def restrict_to_admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("Access denied. Admins only!", "danger")
        return redirect(url_for("main.login"))


@admin_bp.route("/")     
@login_required
def dashboard():
    total_orders = Order.query.count()
    total_books = Book.query.count()
    total_users = User.query.count()
    return render_template(
        "admin_dashboard.html",
        total_orders=total_orders,
        total_books=total_books,
        total_users=total_users,
    )



@admin_bp.route("/orders")   # Manage Orders 
@login_required
def view_orders():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return render_template("admin_orders.html", orders=orders)


@admin_bp.route("/order/<int:order_id>/update", methods=["POST"])
@login_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get("status")
    if new_status in ["Pending", "Shipped", "Delivered", "Cancelled"]:
        order.status = new_status
        db.session.commit()
        flash(f"Order {order.id} updated to {new_status}.", "success")
    else:
        flash("Invalid status!", "danger")
    return redirect(url_for("admin.view_orders"))


@admin_bp.route("/orders/<int:order_id>")
@login_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    buyer = User.query.get(order.user_id)
    total = sum(item.book.price * item.quantity for item in order.items)
    return render_template("admin_order_details.html", order=order, buyer=buyer, total=total)


 
@admin_bp.route("/users")  # Manage Users
@login_required
def manage_users():
    users = User.query.all()
    return render_template("admin_users.html", users=users)


@admin_bp.route("/user/<int:user_id>/promote")
@login_required
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    flash(f"{user.username} promoted to Admin.", "success")
    return redirect(url_for("admin.manage_users"))


@admin_bp.route("/user/<int:user_id>/demote")
@login_required
def demote_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = False
    db.session.commit()
    flash(f"{user.username} demoted to User.", "warning")
    return redirect(url_for("admin.manage_users"))


@admin_bp.route("/user/<int:user_id>/delete")
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "danger")
    return redirect(url_for("admin.manage_users"))



@admin_bp.route("/books")   #  Manage Books 
@login_required
def manage_books():
    books = Book.query.all()
    return render_template("admin_books.html", books=books)

@admin_bp.route("/books/add", methods=["GET", "POST"])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        filename = None
        if form.picture.data:
            filename = secure_filename(form.picture.data.filename)
            path = os.path.join(current_app.root_path, '..', 'static', 'Book_Image', filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            form.picture.data.save(path)
        book = Book(
            title=form.title.data,
            author=form.author.data,
            publication=form.publication.data,
            publication_date=form.publication_date.data,
            language=form.language.data,
            reading_age=form.reading_age.data,
            ISBN=form.ISBN.data,
            content=form.content.data,
            price=form.price.data,
            piece=form.piece.data,
            image_file=filename or 'default_book.jpg'
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added', 'success')
        return redirect(url_for("admin.manage_books"))
    return render_template("add_book.html", form=form)

@admin_bp.route("/books/update/<int:book_id>", methods=["GET", "POST"])
@login_required
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = UpdateBookForm(obj=book)
    if form.validate_on_submit():
        if form.picture.data:
            filename = secure_filename(form.picture.data.filename)
            path = os.path.join(current_app.root_path, '..', 'static', 'Book_Image', filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            form.picture.data.save(path)
            book.image_file = filename
        book.title = form.title.data
        book.author = form.author.data
        book.publication = form.publication.data
        book.publication_date=form.publication_date.data,
        book.language=form.language.data,
        book.reading_age=form.reading_age.data,
        book.ISBN = form.ISBN.data
        book.content = form.content.data
        book.price = form.price.data
        book.piece = form.piece.data
        db.session.commit()
        flash('Book updated', 'success')
        return redirect(url_for("admin.manage_books"))
    return render_template("update_book.html", form=form, book=book)

@admin_bp.route("/books/delete/<int:book_id>")
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted', 'info')
    return redirect(url_for("admin.manage_books"))