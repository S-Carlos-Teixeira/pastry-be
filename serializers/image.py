from marshmallow import fields
from app import ma
from models.image import ImageModel
from models.product import ProductModel

class ImageSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = ImageModel
        load_instance = True
    include_fk=True