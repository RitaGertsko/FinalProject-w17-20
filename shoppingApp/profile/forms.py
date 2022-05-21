from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, RadioField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Optional, Length


class ProfileForm(FlaskForm):
    first_name = StringField(label="First Name: ",
                             validators=[Optional(), Length(min=2, max=15)])
    last_name = StringField(label="Last Name: ", validators=[Optional(), Length(min=2, max=15)])
    email = EmailField(label="Email: ",
                       validators=[Email(message="Email incorrect: "), Optional(),
                                   Length(min=2, max=50)])
    password = PasswordField(label="Password: ",
                             validators=[Optional(), Length(min=2, max=30)])
    confirm_password = PasswordField(label="Confirm Password: ",
                                     validators=[EqualTo('password', message='Passwords must match'), Optional()])
    age = RadioField(label="Age: ",
                     choices=[('14-20', '14-20'), ('20-30', '20-30'), ('30-40', '30-40'), ('40-50', '40-50'),
                              ('+50', '+50')], validators=[Optional()])
    submit = SubmitField(label='Save')