from app import db
from models.base import BaseModel
from models.cart import CartModel


class ProductCartModel (db.Model, BaseModel):
    __tablename__ = "products_cart"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id") )
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id") )
    

    product = db.relationship("ProductModel", back_populates= "carts")
    cart = db.relationship("CartModel", back_populates= "products")