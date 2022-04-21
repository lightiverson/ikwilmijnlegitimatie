# System packages
import requests

# # Third party packages
from loguru import logger

# User defined packages
from app.models import Utrecht, Vleuten

def get_user_position(email: str):
	"""
	Gives the user position in the waitlist.
	Return -1 (in dictionary) if user not found in specific column of database.
	Return -2 if error with database.

	Returns a dictionary of positions of the user.
	Something like:
	{"Utrecht": 4, "Vleuten": -1}
	This means that that specific email is registered for Utrecht (position 4) and not registered for Vleuten.
	"""

	positions = {"Utrecht": 0, "Vleuten": 0}

	# First find the active tables of that email: Utrecht, Vleuten
	try:
		utrecht = Utrecht.query.filter_by(email=email).first()
		vleuten = Vleuten.query.filter_by(email=email).first()
	except:
		return -2

	# Utrecht position
	if utrecht == None:
		positions["Utrecht"] = -1
	else:
		try:
			utrecht_all_data = Utrecht.query.all()
		except:
			return -2
		for user in utrecht_all_data:
			positions["Utrecht"] += 1
			if user.email == email:
				break

	# Vleuten position
	if vleuten == None:
		positions["Vleuten"] = -1
	else:
		try:
			vleuten_all_data = Vleuten.query.all()
		except:
			return -2
		for user in vleuten_all_data:
			positions["Vleuten"] += 1
			if user.email == email:
				break

	return positions


def request_protected(session: requests.Session, method: str, url: str, **kwargs) -> requests.Response:
	"""
	Performs a normal request and protects for errors like HTTP or TIMEOUT.
	
	Arguments:
		- session: the session in which to perform the request.
		- method: HTTP methods: get, post, etc.
		- url: url for the request.
		- kwargs: keyword arguments for the request.

	Returns:
		response of the request or raises an error.
	"""
	try:
		response = session.request(method, url, **kwargs)
		response.raise_for_status()
	except requests.exceptions.HTTPError as errh:
		logger.error(f"HTTP ERROR: {errh}")
	except requests.exceptions.ConnectionError as errc:
		logger.error(f"CONNECTION ERROR: {errc}")
	except requests.exceptions.Timeout as errt:
		logger.error(f"TIMEOUT ERROR: {errt}")
	except requests.exceptions.RequestException as err:
		logger.error(f"OTHER ERROR: {err}")
	return response

