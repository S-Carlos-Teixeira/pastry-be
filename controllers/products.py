from http import HTTPStatus
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError, RegistryError
from flask import Blueprint, request, g
from models.user import UserModel
from models.image import ImageModel
from models.product import ProductModel
from serializers.product import ProductSchema
from serializers.image import ImageSchema
# from serializers.user import UserSchema
from middleware.secure_route import secure_route

# user_schema = UserSchema()
image_schema = ImageSchema()
product_schema = ProductSchema()


router = Blueprint("products", __name__)


@router.route("/products", methods=["GET"])
def get_products():
    try:
        # getting products from db
        products = ProductModel.query.all()
        # returning products
        return product_schema.jsonify(products, many=True), HTTPStatus.OK

    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}


@router.route("/product/<int:prod_id>", methods=["GET"])
def get_product(prod_id):
    try:
        # getting product from db
        product = ProductModel.query.get(prod_id)
        # checking if product exists
        if not product:
            return {"message": "Product not found."}, HTTPStatus.NOT_FOUND
        #
        return product_schema.jsonify(product), HTTPStatus.OK

    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}


@router.route("/product", methods=["POST"])
@secure_route
def create_product():
    try:
        # getting product data from request
        product_dictionary = request.json
        # adding user id to product data
        product_dictionary["created_by"] = g.current_user.id
        # checking if user is not customer
        if g.current_user.role_id >= 4:
            return {"message": "Unauthorized."}, HTTPStatus.UNAUTHORIZED
        # creating product
        product = product_schema.load(product_dictionary, unknown=EXCLUDE)
        # saving product
        product.save()
        # getting image data from request
        image_dictionary = {"product_id": product.id, "image_url": request.json["image_url"]}
        # creating image
        image = image_schema.load(image_dictionary)
        # saving image
        image.save()
        # returning product
        return product_schema.jsonify(product), HTTPStatus.CREATED
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}


@router.route("/product/<int:prod_id>/image", methods=["POST"])
@secure_route
def update_product_image(prod_id):
    try:
        # getting product from db
        product = ProductModel.query.get(prod_id)
        # checking if product exists
        if not product:
            return {"message": "Product not found."}, HTTPStatus.NOT_FOUND
        # checking if user is not customer
        if g.current_user.role_id >= 4:
            return {"message": "Unauthorized."}, HTTPStatus.UNAUTHORIZED
        # getting image data from request
        image_dictionary = {"product_id": product.id, "image_url": request.json["image_url"]}
        # updating image
        image = image_schema.load(image_dictionary)
        # saving image
        image.save()
        # returning product
        return product_schema.jsonify(product), HTTPStatus.OK
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}


@router.route("/product/<int:prod_id>", methods=["PUT", "PATCH"])
@secure_route
def update_product(prod_id):
    try:
        # getting product from db
        product = ProductModel.query.get(prod_id)
        # checking if product exists
        if not product:
            return {"message": "Product not found."}, HTTPStatus.NOT_FOUND
        # checking if user is admin or owner
        if  g.current_user.role_id >= 3:
            return {"message": "Unauthorized."}, HTTPStatus.UNAUTHORIZED
        # getting product data from request
        product_dictionary = request.json
        # updating product
        product = product_schema.load(product_dictionary, instance=product, partial=True, unknown=EXCLUDE)
        # saving product
        product.save()
        # returning product
        return product_schema.jsonify(product), HTTPStatus.OK
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}

@router.route("/product/<int:prod_id>", methods=["DELETE"])
@secure_route
def delete_product(prod_id):
    try:
        #getting user password from request
        user_pass = request.json["password"]
        #getting product from db
        product = ProductModel.query.get(prod_id)
        #getting user from db
        user = UserModel.query.get(g.current_user.id)
        
        #checking if user insert password
        if not user_pass:
            return {"message":"Please insert your password."}, HTTPStatus.UNAUTHORIZED
        #checking if product exists
        if not product:
            return {"message": "Product not found."}, HTTPStatus.NOT_FOUND
        #checking if user is admin or owner
        if user.role_id >=3:
            return {"message": "Unauthorized."}, HTTPStatus.UNAUTHORIZED
        # checking if user password is correct
        if not user.validate_password(user_pass):
            return {"message": "Unauthorized."}, HTTPStatus.UNAUTHORIZED
        # deleting product
        product.remove()
        # returning no content
        return "", HTTPStatus.NO_CONTENT
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}

@router.route("/product/<int:prod_id>/image/<int:image_id>", methods=["DELETE"])
@secure_route
def delete_product_image(prod_id, image_id):
    try:
        #getting product from db
        product = ProductModel.query.get(prod_id)
        #getting image from db
        image = ImageModel.query.get(image_id)
        #getting user from db
        user = UserModel.query.get(g.current_user.id)
        
        #checking if product exists
        if not product:
            return {"message": "Product not found."}, HTTPStatus.NOT_FOUND
        #checking if image exists
        if not image:
            return {"message": "Image not found."}, HTTPStatus.NOT_FOUND
        # checking if image is not product image
        if product.id != image.product_id:
            return {"message": "Unauthorized."}, HTTPStatus.UNAUTHORIZED
        #checking if user is not customer
        if user.role_id >=4:
            return {"message": "Unauthorized."}, HTTPStatus.UNAUTHORIZED
        # deleting product image
        image.remove()
        # returning no content
        return product_schema.jsonify(product), HTTPStatus.ACCEPTED
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}