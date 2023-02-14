from app import db
from models.base import BaseModel

class OrderModel (db.Model, BaseModel):
    __tablename__ = "orders"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    total = db.Column(db.Float, nullable= False)
    status = db.Column(db.Text, default = "pending")
    

    cart = db.relationship("CartModel", back_populates = "order")
    user = db.relationship("UserModel", back_populates = "order")