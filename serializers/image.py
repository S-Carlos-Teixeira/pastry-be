from app import ma
from models.image import ImageModel


class ImageSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = ImageModel
        load_instance = True
        load_only = ("created_at", "updated_at", "product_id")
        include_fk=True