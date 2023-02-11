from models.base import BaseModel
from app import db

class RoleModel(db.Model, BaseModel):
    __tablename__ = "roles"
    role_name = db.Column(db.Text, nullable=False, unique=True)

    user = db.relationship("UserModel", back_populates="role")
    