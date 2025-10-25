from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, FloatField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from .models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    address = StringField('Address', validators=[Length(max=200)])
    state = StringField('State', validators=[Length(max=100)])
    pincode = StringField('Pincode', validators=[Length(max=20)])
    submit = SubmitField('Update')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    author = StringField('Author', validators=[DataRequired(), Length(max=120)])
    publication = StringField('Publication', validators=[Length(max=120)])
    publication_date = DateField('Publication Date', format='%Y-%m-%d')  
    language = StringField('Language', validators=[Length(max=50)])      
    reading_age = StringField('Reading Age', validators=[Length(max=50)]) 
    ISBN = StringField('ISBN', validators=[Length(max=50)])
    content = TextAreaField('Description', validators=[Length(max=1000)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    piece = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    picture = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add Book')

class UpdateBookForm(BookForm):
    submit = SubmitField('Update Book')

class CheckoutForm(FlaskForm):
    submit = SubmitField('Confirm Order')
