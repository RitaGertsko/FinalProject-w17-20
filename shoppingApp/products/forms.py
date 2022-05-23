from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField, BooleanField, SelectMultipleField
from wtforms.validators import InputRequired, Optional, Length


class AddProductForm(FlaskForm):
    title = StringField(label="Title: ",
                        validators=[InputRequired(message='Please enter the product name/title'),
                                    Length(min=2, max=200)])
    description = StringField(label="Description: ", validators=[Optional(), Length(min=5, max=400)])
    ingredients = StringField(label="Ingredients: ", validators=[Optional(), Length(min=5, max=400)])
    price = FloatField(label="Price: ",
                       validators=[InputRequired(message='Please enter product price')])
    img = TextAreaField(label="Img 1: ",
                        validators=[InputRequired(message='Please enter product price')])
    img2 = TextAreaField(label="Img 2: ",
                         validators=[Optional()])
    img3 = TextAreaField(label="Img 3: ",
                         validators=[Optional()])
    sale = BooleanField(label="On sale: ",
                        validators=[Optional()])
    category = SelectMultipleField(label="Category: ", validators=[InputRequired(message='Category must be selected')])
    company = SelectMultipleField(label="Company: ", validators=[InputRequired(message='Company must be selected')])
    submit = SubmitField(label='Add')
