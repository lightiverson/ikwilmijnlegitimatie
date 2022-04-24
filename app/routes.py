# Standard packages
from datetime import datetime

# Third party packages
import sqlalchemy
from flask import render_template, flash, redirect, url_for
from loguru import logger

# Self-defined packages
from app import app, db
from app.forms import DeleteMeForm, RegisterForm, PositionInQueueForm
from app.models import HelpedUsers, Utrecht, Vleuten
from app import utils
from config import Config

# Packages for tracking usage
from flask_track_usage import TrackUsage
from flask_track_usage.storage.sql import SQLStorage

# Track usage
pstore = SQLStorage(db=db)
t = TrackUsage(app, [pstore])

# Setup logger for database exceptions
logger.add(f"logs/database/db.log", retention=None, level="TRACE")

@t.include
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
	register_form = RegisterForm()
	position_form = PositionInQueueForm()
	delete_me_form = DeleteMeForm()

	if register_form.submit.data and register_form.validate():

		# Gather data and hash it
		first_name = Config.fernet.encrypt(register_form.first_name.data.encode())
		last_name = Config.fernet.encrypt(register_form.last_name.data.encode())
		email = register_form.email.data
		date_of_birth = Config.fernet.encrypt(register_form.date_of_birth.data.strftime("%Y-%m-%d").encode())
		phone = Config.fernet.encrypt(register_form.phone.data.encode())
		id_type = register_form.id_type.data
		location = register_form.location.data
		registered_at = datetime.now()

		if register_form.location.data == "Utrecht":
			user = Utrecht(first_name=first_name,
							last_name=last_name,
							email=email,
							date_of_birth=date_of_birth,
							phone=phone,
							id_type=id_type,
							location=location,
							registered_at=registered_at)
		elif register_form.location.data == "Vleuten":
			user = Vleuten(first_name=first_name,
							last_name=last_name,
							email=email,
							date_of_birth=date_of_birth,
							phone=phone,
							id_type=id_type,
							location=location,
							registered_at=registered_at)
		try:
			if register_form.location.data == "Utrecht":
				position = db.session.query(Utrecht).count() + 1
			elif register_form.location.data == "Vleuten":
				position = db.session.query(Vleuten).count() + 1
			if position > Config.MAX_PEOPLE:
				raise utils.LimitReached
			db.session.add(user)
			db.session.commit()
			logger.trace(f"Added: {email} for {location}.")
			flash_message = f"Bedankt voor je registratie voor een {register_form.id_type.data} op locatie {register_form.location.data}! Je huidige positie in de wachtlijst is {position}."
		except utils.LimitReached:
			flash_message = f"Het maximum aantal mensen ({Config.MAX_PEOPLE}) is al aangemeld. Probeer het later opnieuw."
		except sqlalchemy.exc.IntegrityError:
			flash_message = f"Deze email is bij ons al bekend voor een aanvraag op locatie {register_form.location.data}."
		except Exception as err:
			flash_message = f"Oeps, er is een probleem met de webapplicatie. Geen stress, ik ben ermee bezig. Probeer het later opnieuw!"
			logger.error(f"DATABASE_ERROR: {err}.")

		flash(flash_message)
		return redirect(url_for("index"))
		

	if position_form.submit_position.data and position_form.validate():

		logger.trace(f"Asked: {position_form.email.data} for position.")
		positions, id_types = utils.get_user_position(position_form.email.data)
		if positions["Utrecht"] == -1 and positions["Vleuten"] == -1:
			flash_message = f"De ingevoerde emailadres is niet bekend bij ons. Probeer het opnieuw!"
		elif positions == -2:
			flash_message = f"Oeps, er is een probleem met de webapplicatie. Geen stress, ik ben ermee bezig. Probeer het later opnieuw!"
		else:
			flash_message = ""
			for table, position in positions.items():
				if position != -1:
					flash(f"Je huidige positie in de wachtlijst voor een {id_types[table]} in {table} is {position}.")
			return redirect(url_for("index"))

		flash(flash_message)
		return redirect(url_for("index"))

	if delete_me_form.submit_delete.data and delete_me_form.validate():

		# Set table of database
		if delete_me_form.location.data == "Utrecht":
			db_table = Utrecht
		else:
			db_table = Vleuten

		# Find user in table (also decrypt user date of birth for comparison with date of birth from the form)
		user = db_table.query.filter_by(email=delete_me_form.email.data).first()

		if user != None:
			user_date_of_birth_decrypted = Config.fernet.decrypt(user.date_of_birth.encode()).decode()	# when receiving the data back from mysql, we get it back as a string, decrypt() want bytes, so encode it.
		else:
			user_date_of_birth_decrypted = ""

		if user == None or user_date_of_birth_decrypted != delete_me_form.date_of_birth.data.strftime("%Y-%m-%d"):
			flash_message = f"Je staat niet ingeschreven op locatie {delete_me_form.location.data} met email {delete_me_form.email.data} en geboortedatum {delete_me_form.date_of_birth.data}."
		else:
			try:
				db.session.delete(user)
				db.session.commit()
				logger.trace(f"Deleted: {delete_me_form.email.data} for {delete_me_form.location.data}.")
			except:
				flash_message = f"Oeps, er is een probleem met de webapplicatie. Geen stress, ik ben ermee bezig. Probeer het later opnieuw!"
				logger.error(f"DATABASE_ERROR: {delete_me_form.email.data} - {delete_me_form.location.data}.")
			flash_message = f"Je bent uitgeschreven op locatie {delete_me_form.location.data} met email {delete_me_form.email.data}. Jammer..."
		flash(flash_message)
		return redirect(url_for("index"))
	
	return render_template("index.html", 
							title="ikwilmijnlegitimatie",
							register_form=register_form,
							position_form=position_form,
							delete_me_form=delete_me_form,
							total_people_waitlist_utrecht=db.session.query(Utrecht).count(),
							total_people_waitlist_vleuten=db.session.query(Vleuten).count(),
							max_people=Config.MAX_PEOPLE,
							days_to_check=Config.DAYS,
							total_people_helped=db.session.query(HelpedUsers).count())