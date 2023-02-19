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
        
        if not cart:
            return {"message": "Cart not found"}, HTTPStatus.NOT_FOUND
        if not current_user:
            return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
        total = 0
        for cart_item in cart.products:
            product_total = cart_item.product.price * cart_item.quantity
            total += product_total
        order_dictionary = {
            "cart_id": cart.id,
            "user_id": current_user.id,
            "total": total,
        }
        order = OrderModel.query.filter_by(user_id=g.current_user.id, is_active=True
        ).first()
        print(order)
        if not order:
            order = order_schema.load(order_dictionary)
            order.save()
        return order_schema.jsonify(order)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}

@router.route("/order", methods=["PUT", "PATCH"])
@secure_route
def update_order():
    try:
        order_dictionary = request.get_json()
        order = OrderModel.query.filter_by(user_id=g.current_user.id, is_active=True).first()
        if not order:
            return {"message": "Order not found"}, HTTPStatus.NOT_FOUND
        
        cart = CartModel.query.get(order.cart_id)
        if not cart:
            return {"message": "Cart not found"}, HTTPStatus.NOT_FOUND
        
        order = order_schema.load(order_dictionary, instance=order, partial=True)
        order.save()
        if order.status == "paid":
            cart.is_active = False
            cart.save()
        if order.status == "cancelled":
            order.is_active = False
            cart.is_active = False
            order.save()
            cart.save()
        if order.status == "delivered":
            order.is_active = False
            cart.is_active = False
            order.save()
            cart.save()

        return order_schema.jsonify(order)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}
