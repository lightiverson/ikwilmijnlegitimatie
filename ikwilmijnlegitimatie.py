from app import app, db
from app.models import Utrecht, Vleuten
from datetime import datetime

@app.shell_context_processor
def make_shell_context():
	"""
	This function creates a shell context that adds the database instance and Utrecht/Vleuten model to the shell session.
	You can run "flask shell" in the terminal.
	"""
	return {'db': db, 'Utrecht': Utrecht, 'Vleuten': Vleuten, 'datetime': datetime}
