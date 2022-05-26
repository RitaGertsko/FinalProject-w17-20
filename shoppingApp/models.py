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
    title = db.Column(db.String(200), nullable=False, index=True, unique=True)
    description = db.Column(db.Text(), nullable=True)
    ingredients = db.Column(db.Text(), nullable=True)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.Text(), nullable=True)
    img2 = db.Column(db.Text(), nullable=True)
    img3 = db.Column(db.Text(), nullable=True)
    sale = db.Column(db.Boolean, nullable=False, default=False)
    category = db.Column(db.String, db.ForeignKey('categories.category_name'))
    company = db.Column(db.String, db.ForeignKey('companies.company_name'))
    quantity_in_cart = db.Column(db.Integer, default=0, nullable=True)
    cart_id = db.relationship("Cart", back_populates="products")

    def __repr__(self):
        return f"Products('{self.title}', '{self.price}')"


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
    quantity = db.Column(db.Integer, nullable=False, default=1)  # X
    products = db.relationship('Products', back_populates="cart_id") # X

    def __repr__(self):
        return f"Cart('Id: {self.id}','User id:{self.user_id}'')"

    def add_product_to_cart(self, product):
        self.products = product


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(10), nullable=True)
    date_of_registration = db.Column(db.Date, default=date.today())
    admin = db.Column(db.Boolean, default=False)
    cart = db.relationship('Cart', backref='buyer')

    def add_cart_id(self, cart):
        self.cart = cart
        cart.user_id = self

    def __repr__(self):
        return f"User('{self.first_name}','{self.last_name}', '{self.email}','{self.id}')"
