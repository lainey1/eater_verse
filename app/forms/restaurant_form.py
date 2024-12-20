from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Optional, Length,ValidationError



def email_validator(form,field):
    email = field.data
    # if not email.endswith('@something.com'):
    #     raise ValidationError('Email must be from something.com domain.')


class RestaurantForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=95)])
    address = StringField('Address', validators=[InputRequired(), Length(min=1, max=255)])
    city = StringField('City', validators=[InputRequired(), Length(min=1, max=100)])
    state = StringField('State', validators=[InputRequired(), Length(min=1, max=100)])
    country = StringField('Country', validators=[InputRequired(), Length(min=1, max=100)])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(min=10, max=15)])
    email = StringField('Email', validators=[email_validator, Optional(), Length(max=255)])
    website = StringField('Website', validators=[Optional(), Length(max=255)])
    cuisine = StringField('Cuisine', validators=[Optional(), Length(max=50)])
    price_point = SelectField('Price Point', choices=[('1', '$1-$10'), ('2', '$11-$30'), ('3', '$31-$60'), ('4', '$61-$100'), '5', 'Over $100'], validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    # Days of the week with dropdown options for hours
    monday_hours = SelectField('Monday Hours', choices=[('Closed', 'Closed'), ('9am - 5pm', '9am - 5pm'), ('10am - 6pm', '10am - 6pm'), ('12pm - 8pm', '12pm - 8pm'), ('24hrs', '24hrs')], default='Closed')
    tuesday_hours = SelectField('Tuesday Hours', choices=[('Closed', 'Closed'), ('9am - 5pm', '9am - 5pm'), ('10am - 6pm', '10am - 6pm'), ('12pm - 8pm', '12pm - 8pm'), ('24hrs', '24hrs')], default='Closed')
    wednesday_hours = SelectField('Wednesday Hours', choices=[('Closed', 'Closed'), ('9am - 5pm', '9am - 5pm'), ('10am - 6pm', '10am - 6pm'), ('12pm - 8pm', '12pm - 8pm'), ('24hrs', '24hrs')], default='Closed')
    thursday_hours = SelectField('Thursday Hours', choices=[('Closed', 'Closed'), ('9am - 5pm', '9am - 5pm'), ('10am - 6pm', '10am - 6pm'), ('12pm - 8pm', '12pm - 8pm'), ('24hrs', '24hrs')], default='Closed')
    friday_hours = SelectField('Friday Hours', choices=[('Closed', 'Closed'), ('9am - 5pm', '9am - 5pm'), ('10am - 6pm', '10am - 6pm'), ('12pm - 8pm', '12pm - 8pm'), ('24hrs', '24hrs')], default='Closed')
    saturday_hours = SelectField('Saturday Hours', choices=[('Closed', 'Closed'), ('9am - 5pm', '9am - 5pm'), ('10am - 6pm', '10am - 6pm'), ('12pm - 8pm', '12pm - 8pm'), ('24hrs', '24hrs')], default='Closed')
    sunday_hours = SelectField('Sunday Hours', choices=[('Closed', 'Closed'), ('9am - 5pm', '9am - 5pm'), ('10am - 6pm', '10am - 6pm'), ('12pm - 8pm', '12pm - 8pm'), ('24hrs', '24hrs')], default='Closed')
