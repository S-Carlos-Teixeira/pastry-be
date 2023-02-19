from http import HTTPStatus
from marshmallow.exceptions import ValidationError, RegistryError
from flask import Blueprint, request, g
from middleware.secure_route import secure_route
from models.order import OrderModel
from models.cart import CartModel
from serializers.order import OrderSchema

order_schema = OrderSchema()

router = Blueprint("orders", __name__)


@router.route("/orders", methods=["GET"])
@secure_route
def get_order():
    try:
        # get all orders by user
        order = OrderModel.query.filter_by(user_id=g.current_user.id).all()
        # if no order return error
        if not order:
            return {"message": "Order not found"}, HTTPStatus.NOT_FOUND
        # return orders
        return order_schema.jsonify(order, many=True)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}


@router.route("/order", methods=["POST"])
@secure_route
def create_order():
    try:
        # get current user
        current_user = g.current_user
        # if no current user return error
        if not current_user:
            return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
        # get cart by user id and if it is active
        cart = CartModel.query.filter_by(
            user_id=g.current_user.id, is_active=True
        ).first()
        # if no cart return error
        if not cart:
            return {"message": "Cart not found"}, HTTPStatus.NOT_FOUND
        # declare total = 0
        total = 0
        # loop through cart items and get product price and quantity
        for cart_item in cart.products:
            product_total = cart_item.product.price * cart_item.quantity
            # add product total to total
            total += product_total
        #
        order_dictionary = {
            "cart_id": cart.id,
            "user_id": current_user.id,
            "total": total,
        }
        # get order by user id and if it is active and status is pending
        order = OrderModel.query.filter_by(user_id=g.current_user.id, is_active=True, status="pending"
        ).first()
        # if no order create new order
        if not order:
            order = order_schema.load(order_dictionary)
            order.save()
        # return order
        return order_schema.jsonify(order)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}

@router.route("/order/<int:order_id>", methods=["PUT", "PATCH"])
@secure_route
def update_order(order_id):
    try:
        # get order dictionary from request
        order_dictionary = request.get_json()
        # get order by order id
        order = OrderModel.query.get(order_id)
        # if no order return error
        if not order:
            return {"message": "Order not found"}, HTTPStatus.NOT_FOUND
        # get cart by order.cart_id
        cart = CartModel.query.get(order.cart_id)
        # if no cart return error
        if not cart:
            return {"message": "Cart not found"}, HTTPStatus.NOT_FOUND
        # update order
        order = order_schema.load(order_dictionary, instance=order, partial=True)
        order.save()

        # if order status is paid set cart to inactive
        if order.status == "paid":
            cart.is_active = False
            cart.save()
            # get active cart
            is_cart_active = CartModel.query.filter_by(user_id=g.current_user.id, is_active=True).first()
            # if no active cart create new cart
            if not is_cart_active:
                cart = CartModel(user_id=g.current_user.id)
                cart.save()
        # if order status is cancelled set cart and order to inactive
        if order.status == "cancelled":
            order.is_active = False
            cart.is_active = False
            order.save()
            cart.save()
        # if order status is delivered set cart and order to inactive
        if order.status == "delivered":
            order.is_active = False
            cart.is_active = False
            order.save()
            cart.save()
        # return order
        return order_schema.jsonify(order)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}
