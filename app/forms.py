from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, EmailField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from datetime import datetime
from config import Config

class RegisterForm(FlaskForm):
	"""
	This is the form people use to register for the gemeente bot.
	""" 
	email = EmailField("Email", validators=[DataRequired(Config.DATA_REQUIRED_ERROR_MESSAGE), Email(Config.EMAIL_ERROR_MESSAGE), Length(max=Config.MAX_EMAIL_LENGTH)])
	phone = StringField("Phone Number", validators=[DataRequired(Config.DATA_REQUIRED_ERROR_MESSAGE), Length(max=Config.MAX_PHONE_LENGTH)])
	first_name = StringField("Firstname", validators=[DataRequired(Config.DATA_REQUIRED_ERROR_MESSAGE), Length(max=Config.MAX_NAME_LENGTH)])
	last_name = StringField("Lastname", validators=[DataRequired(Config.DATA_REQUIRED_ERROR_MESSAGE), Length(max=Config.MAX_NAME_LENGTH)])
	date_of_birth = DateField("Date of Birth", validators=[DataRequired(Config.DATA_REQUIRED_ERROR_MESSAGE)])
	id_type = SelectField("Legitimatie Type", choices = [('Paspoort', 'Paspoort'), ('Identiteitskaart', 'Identiteitskaart'), ('Rijbewijs', 'Rijbewijs')])
	location = SelectField("Locatie", choices = [('Utrecht', 'Utrecht'), ('Vleuten', 'Vleuten')])
	agree_to_terms = BooleanField("Agree to Terms", default=False)
	submit = SubmitField("Meld mij aan!")

	def validate_phone(self, phone):
		"""
		Validates the phonenumber.
		Should start with 06...
		"""
		if not phone.data.startswith("06"):
			raise ValidationError("Mobiel telefoonnummer moet beginnen met 06")
		if len(phone.data) != 10:
			raise ValidationError("Telefoonnummer moet 10 cijfers bevatten")

	def validate_agree_to_terms(self, agree_to_terms):
		"""
		Validates agree_to_terms checkbox.
		Should be true.
		"""
		if not agree_to_terms.data:
			raise ValidationError("Je moet de voorwaarden accepteren om je aan te melden.")

class PositionInQueueForm(FlaskForm):
	"""
	This is the form people use to check their position in the queue.
	"""
	email = EmailField("Email", validators=[DataRequired(Config.DATA_REQUIRED_ERROR_MESSAGE), Email(Config.EMAIL_ERROR_MESSAGE)])
	submit_position = SubmitField("Check mijn positie!")

class DeleteMeForm(FlaskForm):
	"""
	For people that want to delete themselves from the waitlist.
	"""
	email = EmailField("Email", validators=[DataRequired(Config.DATA_REQUIRED_ERROR_MESSAGE), Email(Config.EMAIL_ERROR_MESSAGE)])
	date_of_birth = DateField("Date of Birth", validators=[DataRequired(Config.DATA_REQUIRED_ERROR_MESSAGE)])
	location = SelectField("Locatie", choices = [('Utrecht', 'Utrecht'), ('Vleuten', 'Vleuten')])
	submit_delete = SubmitField("Afmelden!")