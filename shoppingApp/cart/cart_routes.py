from flask import Blueprint, render_template, url_for, redirect, flash, request
from shoppingApp.main.forms import SearchForm
from flask_login import login_required, current_user
from shoppingApp import db
from shoppingApp.models import Cart, Products

cart = Blueprint('cart', __name__, template_folder='templates', static_folder='static')

nonymous_cart_items = []


@cart.context_processor
def base():
    formSearch = SearchForm()
    return dict(formSearch=formSearch)


@cart.route("/cart", methods=["GET", "POST"])
@login_required
def userCart():
    cart_items = Products.query.join(Cart).add_columns(Products.quantity_in_cart, Products.price, Products.title,
                                                       Products.img,
                                                       Products.id).all()
    total = 0
    for item in cart_items:
        total += float(item.price) * int(item.quantity_in_cart)

    if request.method == "POST":
        qty = request.form.get("qty")
        id_product = request.form.get("id-product")
        cart_item = Products.query.filter(Products.id == id_product).first()
        cart_item.quantity_in_cart = qty
        db.session.commit()
        cart_items = Products.query.join(Cart).add_columns(Products.quantity_in_cart, Products.price, Products.title,
                                                           Products.img,
                                                           Products.id).all()
        total = 0
        for item in cart_items:
            total += float(item.price) * int(item.quantity_in_cart)

    return render_template('cart.html', title='Cart', cart=cart_items, total=round(total, 2))


@cart.route('/addToCart/<int:product_id>')
@login_required
def addToCart(product_id):
    product = Cart.query.filter_by(product_id=product_id).first()
    if product:
        product = Products.query.filter(Products.id == product_id, Products.quantity_in_cart > 0).first()
        product.quantity_in_cart += 1
        db.session.commit()
        flash('Item is already in your cart, 1 more added!', 'success')
    else:
        product = Products.query.filter_by(id=product_id).first()
        Cart(products=product, user_id=current_user.id)
        product.quantity_in_cart = 1
        db.session.commit()
        flash(f'{product.title} has been added to your cart!', 'success')
    return redirect(url_for('cart.userCart'))


@cart.route("/removeFromCart/<int:product_id>")
@login_required
def removeFromCart(product_id):
    product = Products.query.filter(Products.id == product_id, Products.quantity_in_cart > 0).first()
    product.quantity_in_cart = 0
    item_to_remove = Cart.query.filter_by(product_id=product_id, user_id=current_user.id).first()
    db.session.delete(item_to_remove)
    db.session.commit()
    flash(f'{product.title} has been removed from your cart!', 'danger')
    return redirect(url_for('cart.userCart'))
