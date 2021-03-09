from src.models.User import User
from src import db, bcrypt
from src.services.helpers import get_user_by_email


def register_user_svc(new_user, **kwargs):
	"""
	Register new user service
	:param new_user: User query object with new variables to save as a new user.
	:param kwargs:
	:return: user query object
	"""
	user = get_user_by_email(new_user.email)

	if user:
		return None

	user = new_user
	user.password = bcrypt.generate_password_hash(new_user.password).decode("utf-8")

	# user = User()
	# user.email = kwargs["email"]
	# user.username = kwargs["username"]
	# user.first_name = kwargs["f_name"]
	# user.last_name = kwargs["l_name"]
	# user.bio = kwargs["bio"]
	# user.password = bcrypt.generate_password_hash(kwargs["password"]).decode("utf-8")
	db.session.add(user)
	db.session.commit()
	return user


def login_user_svc(login_user, **kwargs):
	"""
	User authentication service.
	Checks the given password against the stored hash.
	:param kwargs:
	:return: user query object
	"""
	user = get_user_by_email(login_user.email)
	if not user or not bcrypt.check_password_hash(user.password, login_user.password):
		return None
	return user
