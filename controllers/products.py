from http import HTTPStatus
from marshmallow.exceptions import ValidationError, RegistryError
from flask import Blueprint, request
# from models.user import UserModel
# from models.image import ImageModel
from models.product import ProductModel
from serializers.product import ProductSchema
# from serializers.image import ImageSchema
# from serializers.user import UserSchema

# user_schema = UserSchema()
# image_schema = ImageSchema()
product_schema = ProductSchema()


router = Blueprint("products", __name__)


@router.route("/products", methods=["GET"])
def get_products():
    try:
        products = ProductModel.query.all()
        return product_schema.jsonify(products, many=True)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}