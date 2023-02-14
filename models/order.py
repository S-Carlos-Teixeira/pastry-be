from app import db
from models.base import BaseModel

class OrderModel (db.Model, BaseModel):
    __tablename__ = "orders"

    
    