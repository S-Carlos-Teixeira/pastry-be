from app import app, db
from models.user import UserModel
from models.role import RoleModel


roles = ["Admin", "Owner", "Employee", "Customer"]
with app.app_context():

    try:
        print("Creating our database...")

        db.session.commit()
        db.drop_all()
        db.create_all()

        print("Seeding the database!")
        for role in roles:
            rolename = RoleModel(role_name=role)
            rolename.save()
        user = UserModel(
            email="carlos@carlos.com",
            username="carlos",
            password="1q2w3e4r5t6Y.",
            name="Carlos",
            surname="Teixeira",
            phone="07767668991",
            role_id=1,
        )
        user.save()
        user_customer = UserModel(
            email="customer@customer.com",
            username="customer",
            password="1q2w3e4r5t6Y.",
            name="Carlos",
            surname="Teixeira",
            phone="07767668999",
        )
        user_customer.save()
        
        print("Database seeded!")
    except Exception as e:
        print("exception", e)
