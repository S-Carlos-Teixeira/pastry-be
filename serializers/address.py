from marshmallow import fields
from app import ma
from models.address import AddressModel

class AddressSchema (ma.SQLAlchemyAutoSchema):

    class Meta:
        model = AddressModel
        load_instance = True
        include_fk = True