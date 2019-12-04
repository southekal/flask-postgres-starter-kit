from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import (
	FileField, 
	FileAllowed, 
	FileRequired
)
from sqlalchemy import func
from wtforms import (
	IntegerField,
	PasswordField,
	SelectField, 
	SelectMultipleField,
	StringField, 
	SubmitField,
	TextAreaField
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
	Email, 
	DataRequired,
	ValidationError
)
from wtforms.widgets import html5

from bin.helper import timestamp_formatter
from bin.helper.models import db_case_insensitive
from log_config.custom_logger import logger

# ============ AUTH FORMS =======================

class RegisterForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	email = EmailField('Email Address', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	clean_tz = timestamp_formatter.convert_tz_for_select_field()
	time_zone = SelectField(choices=clean_tz)
	submit = SubmitField('Get Started')

	def validate_email(self, email):
		user_record = db_case_insensitive.get_user(email=email.data)
		if user_record is not None:
			logger.warning(f"user already exists; {user_record}; input; {email.data}")
			raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
	email = EmailField('Email Address', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Log In')


class SettingsForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	email = EmailField('Email Address', validators=[DataRequired(), Email()])
	clean_tz = timestamp_formatter.convert_tz_for_select_field()
	time_zone = SelectField(choices=clean_tz)
	submit = SubmitField('Update Settings')

# ============ AUTH FORMS =======================

# ============ BETA WAITLIST FORMS =======================
class WaitlistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('submit')

# ============ END OF BETA WAITLIST FORMS =======================





