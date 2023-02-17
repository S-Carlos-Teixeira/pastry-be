from http import HTTPStatus
from flask import Blueprint, request, g
from marshmallow.exceptions import ValidationError
from models.user import UserModel
from serializers.user import UserSchema, UserSignupSchema
from middleware.secure_route import secure_route

user_schema = UserSchema()
user_signup_schema = UserSignupSchema()

router = Blueprint("users", __name__)

@router.route('/signup', methods=["POST"])
def signup():
    user_dictionary = request.json

    try:
        user = user_signup_schema.load(user_dictionary)
        user.save()
        return user_schema.jsonify(user), HTTPStatus.CREATED

    except ValidationError as e:
        return {"errors": e.messages, "messsages": "Something went wrong"}


@router.route('/login', methods=["POST"])
def login():

    user_dictionary = request.json
    user = UserModel.query.filter_by(email=user_dictionary["email"]).first()
    try:
        if not user:
            return { "message": "Your email or password was incorrect." }, HTTPStatus.UNAUTHORIZED
        if not user.validate_password(user_dictionary["password"]):
            return { "message": "Your email or password was incorrect." }, HTTPStatus.UNAUTHORIZED
        token = user.generate_token()
        return { "token": token, "message": "Welcome back!" }, HTTPStatus.OK

    except ValidationError as e:
        return {"errors": e.messages, "messsages": "Something went wrong"}


@router.route("/user", methods=["GET"])
@secure_route
def get_user():
    try:
        user = UserModel.query.get(g.current_user.id)
        return user_signup_schema.jsonify(user), HTTPStatus.OK
    except ValidationError as e:
        return {"errors": e.messages, "messsages": "Something went wrong"}


@router.route("/user", methods=["PUT", "PATCH"])
@secure_route
def update_user():
    user_dictionary = request.json
    user = UserModel.query.get(g.current_user.id)

    if not user:
        return {"message":"Unauthorized"}, HTTPStatus.UNAUTHORIZED

    try:
        updated_user = user_signup_schema.load( user_dictionary, instance= user, partial= True)
        updated_user.save()
        return user_signup_schema.jsonify(updated_user), HTTPStatus.ACCEPTED

    except ValidationError as e:
        return {"errors": e.messages, "messsages": "Something went wrong"}


@router.route("/user", methods= ["DELETE"])
@secure_route
def delete_user():


    try:
        user_pass = request.json
        user = UserModel.query.get(g.current_user.id)
        if not user_pass:
            return {"message":"Please insert your password."}, HTTPStatus.UNAUTHORIZED
        if not user:
            return {"message":"Unauthorized"}, HTTPStatus.UNAUTHORIZED
        if not user.validate_password(user_pass["password"]):
            return { "message": "Your email or password was incorrect." }, HTTPStatus.UNAUTHORIZED
        user.remove()
        return "", HTTPStatus.NO_CONTENT
    except ValidationError as e:
        return {"errors": e.messages, "messsages": "Something went wrong"}
    