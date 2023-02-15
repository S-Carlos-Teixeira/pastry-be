from app import ma
from models.role import RoleModel

class RoleSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = RoleModel
        load_instance = True