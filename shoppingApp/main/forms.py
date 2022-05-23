from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

class SearchForm(FlaskForm):
    word = StringField(label="Search: ",
                       validators=[Length(min=2, max=200)])
    submit = SubmitField('submit')
