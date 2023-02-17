from http import HTTPStatus
from marshmallow.exceptions import ValidationError, RegistryError
from flask import Blueprint, request
from models.cart import CartModel
from models.cart_item import CartItemModel
from serializers.cart import CartSchema
from serializers.cart_item import CartItemSchema

cart_schema = CartSchema()
cart_item_schema = CartItemSchema()

router = Blueprint("carts", __name__)


@router.route("/cart/<int:cart_id>", methods=["GET"])
def get_cart(cart_id):
    try:
        cart = CartModel.query.get(cart_id)
        print(cart)
        return cart_schema.jsonify(cart)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}

@router.route("/cart_item/<int:cart_item_id>", methods=["GET"])
def get_cart_item(cart_item_id):
    try:
        cart = CartItemModel.query.get(cart_item_id)
        return cart_item_schema.jsonify(cart)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}