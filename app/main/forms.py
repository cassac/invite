from flask_wtf import Form
from flask.ext.login import current_user
from wtforms import StringField, SubmitField, FileField, SelectField, IntegerField, validators, PasswordField, BooleanField
from wtforms.widgets import TextArea
from wtforms.fields.html5 import DateField, EmailField

## VARIABLES FOR SelectField
STATUS_CHOICES = [('Unconfirmed', 'Unconfirmed'), ('Yes','Yes'), ('No','No'), ('Maybe', 'Maybe')]

class LoginForm(Form):
	email = StringField('Email/Username', [validators.Required(), validators.Length(1, 64), validators.Email()])
	password = PasswordField('Password', [validators.Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')

class StatusForm(Form):
	status = SelectField("Are you attending?", choices=STATUS_CHOICES)
	submit = SubmitField('Update')

class AddPictureForm(Form):
	pass

class EmailInvitationForm(Form):
	submit = SubmitField('Send Email')
