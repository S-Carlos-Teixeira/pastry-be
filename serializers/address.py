from marshmallow import fields
from app import ma
from models.address import AddressModel

class AddressSchema (ma.SQLAlchemyAutoSchema):

    class Meta:
        model = AddressModel
        load_instance = True
        load_only = ("created_at", "updated_at", "user_id")
        include_fk = True