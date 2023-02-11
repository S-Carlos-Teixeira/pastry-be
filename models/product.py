from app import db
from models.base import BaseModel
from models.image import ImageModel

class ProductModel(db.Model, BaseModel):
    #table name
    __tablename__ = "products"

    #table data
    name = db.Column(db.Text, nullable=False, unique= True )
    description = db.Column(db.Text, nullable=True, unique=False)
    price = db.Column(db.Float, nullable=False, unique=False)
    in_stock = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),nullable=False)

    #relationships

    images = db.relationship("ImageModel", back_populates="product")
    user = db.relationship("UserModel", back_populates="product")