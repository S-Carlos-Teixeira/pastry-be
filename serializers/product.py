from marshmallow import fields
from app import ma
from models.product import ProductModel
from serializers.image import ImageSchema
from serializers.user import UserSchema




class ProductSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = ProductModel
        load_instance = True
        include_fk=True
    images = fields.Nested("ImageSchema", many=True)
    user = fields.Nested("UserSchema")
    