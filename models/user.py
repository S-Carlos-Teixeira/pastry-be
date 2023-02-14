from datetime import datetime, timedelta
import jwt
from sqlalchemy.ext.hybrid import hybrid_property
from app import db, bcrypt
from models.base import BaseModel
from models.product import ProductModel
from models.address import AddressModel
from config.environment import SECRET


class UserModel(db.Model, BaseModel):
    #table name
    __tablename__ = "users"

    #table data
    username = db.Column(db.Text, nullable=False, unique=True)
    name = db.Column(db.Text, nullable=False, unique=False)
    surname = db.Column(db.Text, nullable=False, unique=False)
    phone = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"),nullable=False, default=4)

    #relationships
    role = db.relationship("RoleModel", back_populates="user")
    product = db.relationship("ProductModel", back_populates="user")
    adresses = db.relationship("AddressModel", back_populates="user")
    carts = db.relationship("CartModel", back_populates = "user")

    #methods
    @hybrid_property
    def password(self):
        pass

    @password.setter
    def password(self, password_plaintext):
        encoded_pw = bcrypt.generate_password_hash(password_plaintext)
        self.password_hash = encoded_pw.decode("utf-8")

    def validate_password(self, password_plaintext):
        return bcrypt.check_password_hash(self.password_hash, password_plaintext)

    def generate_token(self):

        payload = {
            "exp": datetime.utcnow() + timedelta(days=7),
            "iat": datetime.utcnow(),
            "sub": self.id,
        }

        token = jwt.encode(payload, SECRET, algorithm="HS256")

        return token
