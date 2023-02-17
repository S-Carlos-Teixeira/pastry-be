from http import HTTPStatus
from marshmallow.exceptions import ValidationError, RegistryError
from flask import Blueprint, request
from models.order import OrderModel
from serializers.order import OrderSchema

order_schema = OrderSchema()

router = Blueprint("orders",__name__)

@router.route("/order/<int:order_id>", methods=["GET"])
def get_order(order_id):
    try:
        order = OrderModel.query.get(order_id)
        return order_schema.jsonify(order)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}