from flask.ext.wtf import Form
from wtforms import StringField, DateTimeField, TextAreaField,  validators
from wtforms.validators import DataRequired


###

class LoggedObservationForm(Form):

    title = StringField('Title', validators=[DataRequired()])
    timestamp = DateTimeField('Date & TIme', validators=[DataRequired()])
    objects = StringField('Objects', validators=[DataRequired()])
    description = TextAreaField('Description')


###

class EditObjectForm(Form):

    name = StringField('Name', validators=[DataRequired()])
    text = TextAreaField('Notes')

###
