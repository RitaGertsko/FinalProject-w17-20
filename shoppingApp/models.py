from shoppingApp import db
from datetime import date
from flask_login import UserMixin


class Slideshow(db.Model):
    __tablename__ = 'slideshow'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String, db.ForeignKey('companies.company_name'))
    image = db.Column(db.Text, nullable=False)


class Articles(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String, db.ForeignKey('categories.category_name'))
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=True)
    articleUrl = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, default=date.today(), nullable=True)


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, index=True, unique=True)
    description = db.Column(db.Text(), nullable=True)
    ingredients = db.Column(db.Text(), nullable=True)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.Text(), nullable=True)
    img2 = db.Column(db.Text(), nullable=True)
    img3 = db.Column(db.Text(), nullable=True)
    sale = db.Column(db.Boolean, nullable=False)
    category = db.Column(db.String, db.ForeignKey('categories.category_name'))
    company = db.Column(db.String, db.ForeignKey('companies.company_name'))
    cart_id = db.relationship("Cart", back_populates="cart_items")
    cart_quantity = db.Column(db.Integer, default=0)


class Categories(db.Model):
    __tablename__ = 'categories'

    category_name = db.Column(db.String(70), nullable=False, unique=True, primary_key=True)
    products = db.relationship('Products', backref='categories', lazy='dynamic')


class Companies(db.Model):
    __tablename__ = 'companies'

    company_name = db.Column(db.String(100), nullable=False, unique=True, index=True, primary_key=True)
    products = db.relationship('Products', backref='companies', lazy='dynamic')


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    cart_items = db.relationship('Products', back_populates="cart_id")
    quantity = db.Column(db.Integer, nullable=True, default=1)


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(10), nullable=True)
    date_of_registration = db.Column(db.Date, default=date.today())
    cart = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=True)
