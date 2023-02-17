from marshmallow import fields
from app import ma
from models.cart import CartModel
from serializers.cart_item import CartItemSchema
from serializers.user import UserSchema

class CartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = CartModel
        load_instance = True
    products = fields.Nested("CartItemSchema", many=True)
    user = fields.Nested("UserSchema")