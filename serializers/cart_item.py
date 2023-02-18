from marshmallow import fields
from app import ma
from models.cart_item import CartItemModel
from serializers.product import ProductForCartSchema

class CartItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = CartItemModel
        load_instance = True
        load_only = ("created_at", "updated_at", "created_by")
    product = fields.Nested("ProductForCartSchema")