from app import db
from models.base import BaseModel

class ImageModel(db.Model, BaseModel):
    image_URL = db.Column(db.Text, nullable=False, unique=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    product = db.relationship("ProductModel", back_populates="images")