from flask import Blueprint, render_template, request, url_for, redirect
from shoppingApp.models import Articles, Slideshow, Products
from shoppingApp.main.forms import SearchForm

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')


@home.route('/')
def index():
    slideshow = Slideshow.query.all()
    first_skin_care_article = Articles.query.filter_by(category='skin care').order_by(Articles.id.desc()).first()
    first_hair_article = Articles.query.filter_by(category='hair').order_by(Articles.id.desc()).first()
    first_makeup_article = Articles.query.filter_by(category='makeup').order_by(Articles.id.desc()).first()

    return render_template('index.html', title='Home', slideshow=slideshow, skin_care_article=first_skin_care_article,
                           hair_article=first_hair_article, makeup_article=first_makeup_article)


@home.context_processor
def base():
    formSearch = SearchForm()
    return dict(formSearch=formSearch)


@home.route("/search_products", methods=['GET', 'POST'])
def search():
    formSearch = SearchForm()
    if formSearch.validate_on_submit:
        if formSearch.data['submit']:
            word_searched = request.form['searched']
            products = Products.query.filter(Products.title.like(f'%{word_searched}%')).all()
            return render_template('search_products.html', form=formSearch, title='Search', products=products)
    return redirect(url_for('home'))
