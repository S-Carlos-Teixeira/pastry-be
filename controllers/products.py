from http import HTTPStatus
from marshmallow.exceptions import ValidationError, RegistryError
from flask import Blueprint, request
from models.product import ProductModel
# from models.image import ImageModel
# from models.user import UserModel
from serializers.product import ProductSchema
from serializers.image import ImageSchema
from serializers.user import UserSchema

product_schema = ProductSchema()
image_schema = ImageSchema()
user_schema = UserSchema()


router = Blueprint("products", __name__)


@router.route("/products", methods=["GET"])
def get_products():
    try:
        products = ProductModel.query.all()
        return product_schema.jsonify(products, many=True)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}
    # except RegistryError as e:
    #     return {"errors":e}