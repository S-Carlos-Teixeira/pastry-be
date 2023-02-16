from marshmallow import fields
from app import ma
from models.product import ProductModel
# from models.image import ImageModel
# from models.user import UserModel

class ProductSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = ProductModel
        load_instance = True
        include_fk=True
    images = fields.Nested("ImageModel", many=True)
    # user = fields.Nested("UserModel")
    