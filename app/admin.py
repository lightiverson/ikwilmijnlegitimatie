# The app
from app import app, db, models

# Flask
from flask import redirect, url_for

# Flask admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, AdminIndexView, expose

# Flask security
from flask_security import Security, SQLAlchemyUserDatastore, current_user, hash_password

# Configuration parameters
from config import Config

# Used for logs page on Admin page
from config import basedir
from datetime import datetime
from typing import List

# Setup Flask security
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

# This function executes after the first request to webapp.
# So to create the admin, make an initial request.
@app.before_first_request
def create_user():
	models.User.query.delete()	# delete the user table (delete the admin)
	db.create_all()
	user_datastore.create_user(email=Config.ADMIN_EMAIL, password=hash_password(Config.ADMIN_PASSWORD))
	db.session.commit()

class UtrechtBotLogsView(BaseView):
	"""
	Logs page of Adminpage.
	"""
	def is_accessible(self):
		return current_user.is_active and current_user.is_authenticated

	@expose('/')
	def index(self):
		todays_logs_utrecht_filename = f"{basedir}/logs/bot/utrecht_{str(datetime.now().date())}.log"
		try:
			with open(todays_logs_utrecht_filename, "r") as f:
				utrecht_log_contents: List[str] = f.readlines()
		except FileNotFoundError:
			utrecht_log_contents = [f"No log files for Utrecht for {str(datetime.now().date())}"]

		return self.render("admin/utrecht_bot_logs.html", utrecht_log_contents=utrecht_log_contents, date=str(datetime.now().date()))

class VleutenBotLogsView(BaseView):
	"""
	Logs page of Adminpage.
	"""
	def is_accessible(self):
		return current_user.is_active and current_user.is_authenticated

	@expose('/')
	def index(self):
		todays_logs_vleuten_filename = f"{basedir}/logs/bot/vleuten_{str(datetime.now().date())}.log"
		try:
			with open(todays_logs_vleuten_filename, "r") as f:
				vleuten_log_contents: List[str] = f.readlines()
		except FileNotFoundError:
			vleuten_log_contents = [f"No log files for Vleuten for {str(datetime.now().date())}"]

		return self.render("admin/vleuten_bot_logs.html", vleuten_log_contents=vleuten_log_contents, date=str(datetime.now().date()))


# class DatabaseLogsView(BaseView):
# 	"""
# 	Logs page of Adminpage containing database logs.
# 	"""
# 	def is_accessible(self):
# 		return current_user.is_active and current_user.is_authenticated

# 	@expose('/')
# 	def index(self):
# 		database_logs_filename = f"{basedir}/logs/database/db.log"
# 		try:
# 			with open(database_logs_filename, "r") as f:
# 				database_log_contents: List[str] = f.readlines()
# 		except FileNotFoundError:
# 			database_log_contents = [f"No log files for database interactions."]
# 		return self.render("admin/database_logs.html", database_log_contents=database_log_contents)


class MyHomeView(AdminIndexView):
	"""
	The homepage of the Adminpage.
	"""
	def is_accessible(self):
		return current_user.is_active and current_user.is_authenticated

	def _handle_view(self, name):
		if not self.is_accessible():
			return redirect(url_for('security.login'))

	@expose('/')
	def index(self):
		arg1 = 'Hello'
		return self.render('admin/home.html', arg1=arg1)

class AdminModelView(ModelView):
	"""
	Makes sure the user is authenticated (logged in) before showing admin page containing database tables.
	"""
	def is_accessible(self):
		return current_user.is_active and current_user.is_authenticated

	column_exclude_list = ('first_name', 'last_name', "phone", "date_of_birth")


# Create admin page
admin = Admin(app, index_view=MyHomeView())

# Add model view
admin.add_view(AdminModelView(models.Utrecht, db.session, name="Utrecht", endpoint='utrecht'))
admin.add_view(AdminModelView(models.Vleuten, db.session, name="Vleuten", endpoint='vleuten'))
admin.add_view(AdminModelView(models.HelpedUsers, db.session, name="Helpedusers", endpoint='helpedusers'))
admin.add_view(AdminModelView(models.ProblemUsers, db.session, name="Problemusers", endpoint='problemusers'))
admin.add_view(UtrechtBotLogsView(name='UtrechtBotLogs', endpoint='utrecht_bot_logs'))
admin.add_view(VleutenBotLogsView(name='VleutenBotLogs', endpoint='vleuten_bot_logs'))
# admin.add_view(DatabaseLogsView(name='DatabaseLogs', endpoint='db_logs'))

