from http import HTTPStatus
from datetime import datetime
from flask import Blueprint, request, g
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError
from models.user import UserModel
from models.cart import CartModel
from serializers.user import UserSchema, UserSignupSchema, FullUserSchema
from middleware.secure_route import secure_route

user_schema = UserSchema()
user_signup_schema = UserSignupSchema()
full_user_schema = FullUserSchema()

router = Blueprint("users", __name__)


@router.route("/signup", methods=["POST"])
def signup():
    

    try:
        # get the user from the request
        user_dictionary = request.json
        # create the user
        user = user_signup_schema.load(user_dictionary, unknown=EXCLUDE)
        user.save()
        # return the user
        return user_schema.jsonify(user), HTTPStatus.CREATED

    except ValidationError as e:
        return {"errors": e.messages, "messsages": "Something went wrong"}


@router.route("/login", methods=["POST"])
def login():

    try:
        # get the user from the request
        user_dictionary = request.json
        # if user dictionary is empty return error
        if not user_dictionary:
            return {
                "message": "Your email or password was incorrect."
            }, HTTPStatus.UNAUTHORIZED
        # get the user from the database
        user = UserModel.query.filter_by(email=user_dictionary["email"]).first()
        # check if the user exists
        if not user:
            return {
                "message": "Your email or password was incorrect."
            }, HTTPStatus.UNAUTHORIZED
        # check if the password is correct
        if not user.validate_password(user_dictionary["password"]):
            return {
                "message": "Your email or password was incorrect."
            }, HTTPStatus.UNAUTHORIZED
                    
        # generate a token
        token = user.generate_token()
        # get the user cart
        cart = CartModel.query.filter_by(user_id=user.id, is_active=True).first()
        # check if the user has a cart and if it is expired and create one if it is expired or doesn't exist
        if not cart or cart.is_expired(datetime.utcnow()):
            cart = CartModel(user_id=user.id)
            cart.save()
        # return the token
        return {"token": token, "message": "Welcome back!"}, HTTPStatus.OK

    except ValidationError as e:
        return {"errors": e.messages, "messsages": "Something went wrong"}


@router.route("/user", methods=["GET"])
@secure_route
def get_user():
    try:
        # get the current user
        user = UserModel.query.get(g.current_user.id)
        if not user:
            return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
        # return the user
        return full_user_schema.jsonify(user), HTTPStatus.OK
    except ValidationError as e:
        return {"errors": e.messages, "messsages": "Something went wrong"}


@router.route("/user", methods=["PUT", "PATCH"])
@secure_route
def update_user():
    try:
        # get the user from the request
        user_dictionary = request.json
        # get the current user
        user = UserModel.query.get(g.current_user.id)
        # check if the user exists
        if not user:
            return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
        # update the user
        updated_user = user_signup_schema.load(
            user_dictionary, instance=user, partial=True
        )
        # save the user
        updated_user.save()
        # return the updated user
        return user_signup_schema.jsonify(updated_user), HTTPStatus.ACCEPTED

    except ValidationError as e:
        return {"errors": e.messages, "messsages": "Something went wrong"}


@router.route("/user/<int:user_id>", methods=["DELETE"])
@secure_route
def delete_user(user_id):
    try:
        # get the user password from the request
        user_pass = request.json
        # get the user from the database
        user = UserModel.query.get(user_id)
        # get the current user from the database
        current_user = UserModel.query.get(g.current_user.id)
        # check if the user exists
        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND
        # check if password is in the request
        if not user_pass["password"]:
            return {"message": "Please enter your password"}, HTTPStatus.UNAUTHORIZED
        # check if the current user is an admin and its password is correct
        if current_user.role_id == 1 and current_user.validate_password(
            user_pass["password"]
        ):
            user.remove()
            return "", HTTPStatus.NO_CONTENT
        # check if the current user is the user to be deleted and its password is correct
        if (
            current_user.role_id >= 2
            and user.validate_password(user_pass["password"])
            and current_user.id == user_id
        ):
            user.remove()
            return "", HTTPStatus.NO_CONTENT
        #
        else:
            return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
    except ValidationError as e:
        return {"errors": e.messages, "messsages": "Something went wrong"}
