from flask import Blueprint, render_template
from shoppingApp.main.forms import SearchForm

errors = Blueprint('errors', __name__, template_folder='templates', static_folder='static')


@errors.context_processor
def base():
    formSearch = SearchForm()
    return dict(formSearch=formSearch)


@errors.app_errorhandler(404)
def error_404(err):
    formSearch = SearchForm()
    return render_template("404_error.html", formSearch=formSearch), 404