from src.models import User


def get_user_by_username(username):
	"""
	Get user by username helper
	:param username:
	:return: user query object
	"""
	user = User.query.filter_by(username=username).first()
	return user


def get_user_by_id(id):
	"""
	Get user by id helper
	:param id:
	:return: user query object
	"""
	user = User.query.get(id)
	return user


def get_user_by_email(email):
	"""
	Get user by email helper.
	:param email:
	:return: user query object
	"""
	user = User.query.filter_by(email=email).first()
	return user

