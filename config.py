import os
import json
from cryptography.fernet import Fernet

# main directory of application
basedir = os.path.abspath(os.path.dirname(__file__))

# Read the configuration parameters
with open("/etc/ikwilmijnlegitimatie_config.json") as config_file:
	config = json.load(config_file)

class Config(object):

	# Secret key needed with Flask and encryption
	SECRET_KEY = config.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = config.get('DATABASE_URL')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Admin credentials
	# When changed, flask app needs to restart
	ADMIN_EMAIL = config.get('ADMIN_EMAIL')
	ADMIN_PASSWORD = config.get('ADMIN_PASSWORD')

	# Needed for hashing password.
	SECURITY_PASSWORD_SALT = config.get("SECURITY_PASSWORD_SALT")

	# Max number of characters for input (in the form)
	MAX_NAME_LENGTH = 64
	MAX_EMAIL_LENGTH = 128
	MAX_PHONE_LENGTH = 10

	# Max number of characters for input (in the database)
	MAX_NAME_LENGTH_ENCRYPTED = 256
	MAX_EMAIL_LENGTH_ENCRYPTED = 128
	MAX_PHONE_LENGTH_ENCRYPTED = 256

	# Error messages to user
	DATA_REQUIRED_ERROR_MESSAGE = "Dit veld is verplicht."
	EMAIL_ERROR_MESSAGE = "Ongeldig email adres."

	# Max people that can sign up for the bot
	MAX_PEOPLE = 100

	# Redirect to adminpage when Flask-security login is accepted
	SECURITY_POST_LOGIN_VIEW = "/admin"

	# Redirect to login page when logging out with Flask-security
	SECURITY_POST_LOGOUT_VIEW = "/login"

	# Dont allow registrations
	SECURITY_REGISTERABLE = False

	# Fernet object for hashing sensitive data
	fernet = Fernet(SECRET_KEY)

	# For usage tracking
	TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS = "include"

	# Days to check ahead with the bot
	DAYS = 7
