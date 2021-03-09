from src import db
from src.services.helpers import get_user_by_id, get_user_by_username, get_user_by_email
from src.services.file_services import FileService


def get_profile(username):
	"""
	Returns a users profile
	:param username: username of the user to be matched
	:type username: string
	:return: user query object or False
	"""
	user = get_user_by_username(username)
	if user is None:
		return False
	return user


def save_user_settings(id, user_settings, profile_picture, suffix=None):
	"""
	Updates user profile settings.
	:param user_settings: User query object.
	:param profile_picture: Profile picture from flask request
	:param suffix: file extension
	:return: user query object or None
	"""
	try:
		user = get_user_by_id(id)
		for key, value in user_settings.items():
			setattr(user, key, value)
		if profile_picture:
			user.profile_picture = FileService.image_save(
					profile_picture,
					suffix,
					user.id,
					'user_image'
				)
		db.session.commit()
		return user
	except Exception as e:
		# add logging
		print(e)
		return None

