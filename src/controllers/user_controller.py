from src.schemas.UserSchema import user_schema, logged_in_user_schema
from src.models.User import User
from src.services import get_user_by_username, get_user_by_email, get_profile, save_user_settings
from flask import Blueprint, request, jsonify, redirect, url_for, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from pathlib import Path

user = Blueprint('user', __name__, url_prefix="/api/profile")


@user.route("/<string:username>", methods=["GET"])
def profile(username):
	# Retrieve user profile
	this_user = get_profile(username)
	return jsonify(user_schema.dump(this_user))


@user.route("/<string:username>/settings", methods=["GET"])
@jwt_required
def get_profile_settings(username):
	# Get user profile settings
	current_user = get_jwt_identity()
	this_user = User.query.get(current_user)
	print(this_user)
	return jsonify(logged_in_user_schema.dump(this_user)), 200


@user.route("/<string:username>/settings", methods=["PUT", "PATCH"])
@jwt_required
def save_profile_settings(username):
	# Set user settings
	current_user = get_jwt_identity()
	this_user = get_user_by_username(username)
	if this_user.id == current_user:
		user_settings = logged_in_user_schema.load(request.form, partial=True)
		suffix = None
		profile_picture = None
		if request.files:
			profile_picture = request.files["image"]
			suffix = Path(profile_picture.filename).suffix
			if suffix not in [".png", ".jpeg", ".jpg", ".gif"]:
				return abort(400, description="Invalid file type")
		if save_user_settings(current_user, user_settings, profile_picture, suffix) is not None:
			return redirect(url_for('user.get_profile_settings', username=this_user.username)), 200
		else:
			return abort(404)
	return jsonify({"msg": "Not authorized"}), 401
