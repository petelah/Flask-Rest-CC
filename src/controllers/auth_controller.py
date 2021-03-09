import logging

from flask import Blueprint, abort, jsonify, request, redirect, url_for
from src.schemas.UserSchema import user_schema
from flask_jwt_extended import create_access_token, jwt_optional, get_jwt_identity
from src.services.auth_services import register_user_svc, login_user_svc
from datetime import timedelta, datetime as dt

auth = Blueprint("auth",  __name__,  url_prefix="/api/auth")


@auth.route("/register", methods=["POST"])
@jwt_optional
def auth_register():
    current_user = get_jwt_identity()
    if current_user:
        return redirect(url_for("user.profile"))
    new_user = user_schema.load(request.json)
    user = register_user_svc(new_user)
    if user is None:
        return abort(400, description="Email already registered")

    return jsonify(user_schema.dump(user))


@auth.route("/login", methods=["POST"])
def auth_login():
    user = login_user_svc(user_schema.load(request.json, partial=True))
    if not user:
        return abort(401, description="Incorrect username and password")
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=user.id, expires_delta=expiry)
    logger = logging.getLogger('login')
    logger.warning('User %s logged in @ [%s], IP: %s.',
                   user.username,
                   dt.now().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
                   request.remote_addr
                   )
    
    return jsonify({ "token": access_token })

