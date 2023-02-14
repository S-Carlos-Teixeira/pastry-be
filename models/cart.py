from app import db
from models.base import BaseModel


class CartModel (db.Model, BaseModel):
    __tablename__ = "carts"
    is_checked_out = db.Column(db.Boolean, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    products = db.relationship("ProductCartModel", back_populates="cart")

    user = db.relationship("UserModel", back_populates = "carts")