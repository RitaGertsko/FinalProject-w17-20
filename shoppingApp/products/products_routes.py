from shoppingApp import db
from flask import render_template, Blueprint, flash, url_for, redirect
from shoppingApp.main.forms import SearchForm
from shoppingApp.models import Products, Categories, User, Companies
from flask_login import login_required, current_user
from shoppingApp.products.forms import AddProductForm

product = Blueprint('product', __name__, template_folder='templates', static_folder='static')


@product.context_processor
def base():
    formSearch = SearchForm()
    return dict(formSearch=formSearch)


@product.route('/skin_care', methods=['GET', 'POST'])
def skinCare():
    selected_product = Products.query.filter(Products.category == 'skin care')
    return render_template('skin_care.html', title='Skin Care', products=selected_product)


@product.route('/hair_products', methods=['GET', 'POST'])
def hairCare():
    selected_product = Products.query.filter(Products.category == 'hair')
    return render_template('hair_care.html', title='Hair Care', products=selected_product)


@product.route('/makeup_products', methods=['GET', 'POST'])
def makeupProducts():
    selected_product = Products.query.filter(Products.category == 'makeup')
    return render_template('makeup_products.html', title='Makeup Products', products=selected_product)


@product.route('/body_products', methods=['GET', 'POST'])
def bodyCare():
    selected_product = Products.query.filter(Products.category == 'body')
    return render_template('body_products.html', title='Body Care', products=selected_product)


@product.route('/product_info/<int:product_id>', methods=['GET'])
def productInfo(product_id):
    selected_product = Products.query.filter_by(id=product_id).first()
    return render_template('product_info.html', title='Product Info', product=selected_product)


@product.route('/add_product', methods=['GET', 'POST'])
@login_required
def addProduct():
    user = User.query.get(current_user.id)

    form = AddProductForm()

    products = Products.query.all()

    if user.admin:
        categories_choices = [choice.category_name for choice in Categories.query.all()]
        companies_choices = [choice.company_name for choice in Companies.query.all()]

        form.category.choices = categories_choices
        form.company.choices = companies_choices

        if form.validate_on_submit():
            selected_category = [Categories.query.get(category)
                                 for category in form.category.data]

            selected_company = [Companies.query.get(company)
                                for company in form.company.data]

            new_product = Products(title=str(form.title.data), description=str(form.description.data),
                                   ingredients=str(form.ingredients.data), price=float(form.price.data),
                                   img=str(form.img.data),
                                   img2=str(form.img2.data), img3=str(form.img3.data), sale=bool(form.sale.data),
                                   category=str(selected_category[0].category_name),
                                   company=str(selected_company[0].company_name))

            try:
                db.session.add(new_product)
                db.session.commit()
                flash(f'{new_product.title} has been added!', 'success')
                return redirect(url_for('product.addProduct'))
            except:
                db.session.rollback()
                flash('Product already exists in the database!', 'danger')

    return render_template('manage_products.html', title='Add Products', form=form, user=user, products=products)


@product.route("/remove_product/<int:product_id>")
@login_required
def removeProduct(product_id):
    item_to_remove = Products.query.filter_by(id=product_id).first()
    db.session.delete(item_to_remove)
    db.session.commit()
    flash(f'{item_to_remove.title} has been removed from the database!', 'danger')
    return redirect(url_for('product.addProduct'))
