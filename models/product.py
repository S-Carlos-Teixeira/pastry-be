from app import db
from models.base import BaseModel
from models.image import ImageModel
from models.cart_item import CartItemModel
from models.user import UserModel


class ProductModel(db.Model, BaseModel):
    #table name
    __tablename__ = "products"

    #table data
    name = db.Column(db.Text, nullable=False, unique= True )
    description = db.Column(db.Text, nullable=True, unique=False)
    price = db.Column(db.Float, nullable=False, unique=False)
    in_stock = db.Column(db.Boolean, nullable=False, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"),nullable=True)

    #relationships

    images = db.relationship("ImageModel", back_populates="product", cascade="all, delete-orphan")
    user = db.relationship("UserModel", back_populates="product")
    carts = db.relationship("CartItemModel", back_populates="product")