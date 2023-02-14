from models.base import BaseModel
from app import db

class AddressModel (db.Model, BaseModel):
    __tablename__= "adresses"

    country = db.Column(db.Text, nullable=False )
    fullname = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=True)
    postcode = db.Column(db.Text, nullable=False)
    address_line_1 = db.Column(db.Text, nullable=False)
    address_line_2 = db.Column(db.Text, nullable=True)
    town_city = db.Column(db.Text, nullable=False)
    county = db.Column(db.Text, nullable=True)
    delivery_instr = db.Column(db.Text, nullable=True)
    is_default = db.Column(db.Boolean, nullable=False)
    is_billing_address = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel", back_populates="adresses")