from flask_wtf import FlaskForm
from wtforms import StringField, validators , ValidationError


# **********************************************
# Custon VAlidation
    
def AlphaNum(form, field):
    if not field.data.isalnum():
        raise ValidationError('Only characters and numbers are allowed')
    
def Digit(form, field):
    if not field.data.isdigit():
        raise ValidationError("Only Numbers are allowed")

def Alpha(form, field):
    if not field.data.isalpha():
        raise ValidationError("Only characters are allowed")
    
class ContactForm(FlaskForm):
    name = StringField('name',validators=[validators.DataRequired(),validators.Length(min=3, max=15),AlphaNum])
    number = StringField('number', validators=[validators.DataRequired(), validators.Length(min=10, max=10),Digit])
    city = StringField('city', validators=[validators.data_required(),validators.Length(min=3, max=15),Alpha])



