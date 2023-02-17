from marshmallow import fields
from app import ma
from models.order import OrderModel
from serializers.cart import CartSchema

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderModel
        load_instance = True
        include_fk=True
    cart = fields.Nested("CartSchema")      