from http import HTTPStatus
from marshmallow.exceptions import ValidationError, RegistryError
from flask import Blueprint, request, g
from middleware.secure_route import secure_route
from models.order import OrderModel
from models.cart import CartModel
from serializers.order import OrderSchema

order_schema = OrderSchema()

router = Blueprint("orders", __name__)


@router.route("/order", methods=["GET"])
@secure_route
def get_order():
    try:

        order = OrderModel.query.filter_by(user_id=g.current_user.id).first()

        if not order:
            return {"message": "Order not found"}, HTTPStatus.NOT_FOUND
        return order_schema.jsonify(order)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}


@router.route("/order", methods=["POST"])
@secure_route
def create_order():
    try:
        cart = CartModel.query.filter_by(
            user_id=g.current_user.id, is_active=True
        ).first()
        current_user = g.current_user
        total = 0
        for product in cart.products:
            product_total = product.product.price * product.quantity
            total += product_total

        order_dictionary = {
            "cart_id": cart.id,
            "user_id": current_user.id,
            "total": total,
        }
        order = order_schema.load(order_dictionary)
        order.save()
        return order_schema.jsonify(order)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}
