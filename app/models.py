from app import db
from config import Config
from flask_security.models import fsqla_v2 as fsqla

class Utrecht(db.Model):
	"""
	Utrecht model (table) in the database.
	For appointments in Stadskantoor, Stadsplateau 1, Utrecht.
	"""
	id = db.Column(db.Integer, primary_key=True)					# primary key uniquely identifies each record in table
	first_name = db.Column(db.String(Config.MAX_NAME_LENGTH_ENCRYPTED), index=True)	# unique does the same as primary key
	last_name = db.Column(db.String(Config.MAX_NAME_LENGTH_ENCRYPTED), index=True)
	email = db.Column(db.String(Config.MAX_EMAIL_LENGTH), index=True, unique=True)
	date_of_birth = db.Column(db.String(Config.MAX_NAME_LENGTH_ENCRYPTED), index=True)
	phone = db.Column(db.String(Config.MAX_PHONE_LENGTH_ENCRYPTED), index=True)
	id_type = db.Column(db.String(Config.MAX_NAME_LENGTH), index=True)
	location = db.Column(db.String(Config.MAX_NAME_LENGTH), index=True)
	registered_at = db.Column(db.DateTime, index=True)

	def __repr__(self):
		return f"<{self.email}> <Utrecht>"

class Vleuten(db.Model):
	"""
	Vleuten model (table) in the database.
	For appointments in Wijkservicecentrum Vleuten - De Meern, Dorpsplein 1, Vleuten.
	"""
	id = db.Column(db.Integer, primary_key=True)					# primary key uniquely identifies each record in table
	first_name = db.Column(db.String(Config.MAX_NAME_LENGTH_ENCRYPTED), index=True)	# unique does the same as primary key
	last_name = db.Column(db.String(Config.MAX_NAME_LENGTH_ENCRYPTED), index=True)
	email = db.Column(db.String(Config.MAX_EMAIL_LENGTH), index=True, unique=True)
	date_of_birth = db.Column(db.String(Config.MAX_NAME_LENGTH_ENCRYPTED), index=True)
	phone = db.Column(db.String(Config.MAX_PHONE_LENGTH_ENCRYPTED), index=True)
	id_type = db.Column(db.String(Config.MAX_NAME_LENGTH), index=True)
	location = db.Column(db.String(Config.MAX_NAME_LENGTH), index=True)
	registered_at = db.Column(db.DateTime, index=True)

	def __repr__(self):
		return f"<{self.email}> <Vleuten>"

class HelpedUsers(db.Model):
	"""
	This database table contains users that are helped by ikwilmijnlegitimatie.
	"""
	id = db.Column(db.Integer, primary_key=True)
	id_type = db.Column(db.String(Config.MAX_NAME_LENGTH), index=True)
	location = db.Column(db.String(Config.MAX_NAME_LENGTH), index=True)
	registered_at = db.Column(db.DateTime, index=True)
	got_appointment_at = db.Column(db.DateTime, index=True)	# at which time did the bot get the appointment for the user
	appointment_date = db.Column(db.DateTime, index=True)	# at which time and date is the appointment

	def __repr__(self):
		return f"<{self.email}> <HelpedUsers>"

class ProblemUsers(db.Model):
	"""
	This table saves people for which the bot had problems booking the appointment.
	"""
	id = db.Column(db.Integer, primary_key=True)					# primary key uniquely identifies each record in table
	first_name = db.Column(db.String(Config.MAX_NAME_LENGTH_ENCRYPTED), index=True)	# unique does the same as primary key
	last_name = db.Column(db.String(Config.MAX_NAME_LENGTH_ENCRYPTED), index=True)
	email = db.Column(db.String(Config.MAX_EMAIL_LENGTH), index=True, unique=True)
	date_of_birth = db.Column(db.String(Config.MAX_NAME_LENGTH_ENCRYPTED), index=True)
	phone = db.Column(db.String(Config.MAX_PHONE_LENGTH_ENCRYPTED), index=True)
	id_type = db.Column(db.String(Config.MAX_NAME_LENGTH), index=True)
	location = db.Column(db.String(Config.MAX_NAME_LENGTH), index=True)
	registered_at = db.Column(db.DateTime, index=True)

	def __repr__(self):
		return f"<{self.email}> <ProblemUser>"

# Define models for a secure Admin page (Flask-security-too)
fsqla.FsModels.set_db_info(db)

class Role(db.Model, fsqla.FsRoleMixin):
	pass

class User(db.Model, fsqla.FsUserMixin):
    pass