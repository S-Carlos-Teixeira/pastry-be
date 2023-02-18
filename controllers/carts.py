from http import HTTPStatus
from datetime import datetime
from marshmallow.exceptions import ValidationError, RegistryError
from flask import Blueprint, request, g
from middleware.secure_route import secure_route
from models.product import ProductModel
from models.cart import CartModel
from models.cart_item import CartItemModel
from serializers.cart import CartSchema
from serializers.cart_item import CartItemSchema

cart_schema = CartSchema()
cart_item_schema = CartItemSchema()

router = Blueprint("carts", __name__)


@router.route("/cart", methods=["GET"])
@secure_route
def get_cart():
    try:
        current_user = g.current_user
        cart = CartModel.query.filter_by(user_id=current_user.id, is_active= True).first()

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

@router.route("/cart_item/product/<int:product_id>", methods=["POST"])
@secure_route
def create_cart_item(product_id):
    try:
        # get current user
        current_user = g.current_user
        # get cart
        cart = CartModel.query.filter_by(user_id=current_user.id, is_active= True).first()
        # get product
        product = ProductModel.query.get(product_id)
        # get cart item
        cart_item = CartItemModel.query.filter_by(cart_id=cart.id, product_id=product.id).first()
        # if no cart, create one
        if not cart:
            return {"errors": "Cart not found"}, HTTPStatus.NOT_FOUND
        # if no product or product not avaliable return error
        if not product or not product.in_stock :
            return {"errors": "Product not found"}, HTTPStatus.NOT_FOUND
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
            return cart_schema.jsonify(cart)
        # create cart item
        cart_item = cart_item_schema.load(request.json)
        # add cart_id and product_id to cart_item
        cart_item.cart_id = cart.id
        cart_item.product_id = product.id
        # save cart_item
        cart_item.save()
        # return cart
        return cart_schema.jsonify(cart)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}


@router.route("/cart_item/<int:cart_item_id>", methods=["PUT", "PATCH"])
@secure_route
def update_cart_item(cart_item_id):
    try:
        # get current user
        current_user = g.current_user
        # get cart
        cart = CartModel.query.filter_by(user_id=current_user.id, is_active= True).first()
        # get cart item
        cart_item = CartItemModel.query.filter_by(id=cart_item_id, cart_id=cart.id).first()
        # if no cart, create one
        if not cart:
            return {"errors": "Cart not found"}, HTTPStatus.NOT_FOUND
        # if no cart_item return error
        if not cart_item:
            return {"errors": "Cart item not found"}, HTTPStatus.NOT_FOUND
        # update cart_item
        cart_item = cart_item_schema.load(request.json, instance=cart_item, partial=True)
        # save cart_item
        cart_item.save()
        # return cart
        return cart_schema.jsonify(cart)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}

@router.route("/cart_item/<int:cart_item_id>", methods=["DELETE"])
@secure_route
def delete_cart_item(cart_item_id):
    try:
        # get current user
        current_user = g.current_user
        # get cart
        cart = CartModel.query.filter_by(user_id=current_user.id, is_active= True).first()
        # get cart item
        cart_item = CartItemModel.query.filter_by(id=cart_item_id, cart_id=cart.id).first()
        # if no cart, create one
        if not cart:
            return {"errors": "Cart not found"}, HTTPStatus.NOT_FOUND
        # if no cart_item return error
        if not cart_item:
            return {"errors": "Cart item not found"}, HTTPStatus.NOT_FOUND
        # delete cart_item
        cart_item.remove()
        # return cart
        return cart_schema.jsonify(cart)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}
