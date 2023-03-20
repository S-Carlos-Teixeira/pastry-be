import re
from marshmallow import fields, ValidationError, EXCLUDE
from app import ma
from models.user import UserModel
from serializers.address import AddressSchema


def validate_password(password):

    if len(password) < 8:
        raise ValidationError("Make sure your password is at least 8 characters.")
    elif re.search("[A-Z]", password) is None:
        raise ValidationError("Make sure your password contains a capital letter.")

class UserSchema(ma.SQLAlchemyAutoSchema):

    password = fields.Str(required=True, validate=validate_password)


    class Meta:
        model = UserModel
        load_instance = True
        exclude = ("password_hash", "name", "surname", "phone", "email")
        load_only = ("email", "password", "created_at", "updated_at")
        include_fk = True


class UserSignupSchema(ma.SQLAlchemyAutoSchema):
    password = fields.Str(required=True, validate=validate_password)
    class Meta:
        model = UserModel
        load_instance = True
        exclude = ("password_hash","role_id")
        unknown = EXCLUDE
        load_only = ("email", "password", "created_at", "updated_at")
        include_fk = True


class FullUserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = UserModel
        load_instance = True
        exclude = ("password_hash",)
        unknown = EXCLUDE
        load_only = ("password", "created_at", "updated_at", "id")
        include_fk = True
    adresses = fields.Nested("AddressSchema", many=True)