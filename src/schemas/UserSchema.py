from src import ma
from src.models import User
from marshmallow.validate import Length, Email


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = [
            "first_name",
            "last_name",
            "email",
            "password"
        ]
        load_instance = True
    
    email = ma.String(required=True, validate=[Length(min=4), Email()])
    username = ma.String(required=True, validate=[Length(min=1)])
    first_name = ma.String(required=True, validate=[Length(min=2)])
    last_name = ma.String(required=True, validate=[Length(min=2)])
    password = ma.String(required=True, validate=Length(min=6))


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class LoggedInUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = [
            "password"
        ]

    email = ma.String(required=True, validate=[Length(min=4), Email()])
    username = ma.String(required=True, validate=[Length(min=1)])
    first_name = ma.String(required=True, validate=[Length(min=2)])
    last_name = ma.String(required=True, validate=[Length(min=2)])
    password = ma.String(required=True, validate=Length(min=6))


logged_in_user_schema = LoggedInUserSchema()
