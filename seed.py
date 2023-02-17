from app import app, db
from models.user import UserModel
from models.role import RoleModel
from models.product import ProductModel
from models.image import ImageModel
from models.address import AddressModel
from models.cart import CartModel
from models.cart_item import CartItemModel
from models.order import OrderModel


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

        address = AddressModel(
            country = "Monaco",
            fullname = user_customer.name + " " +user_customer.surname,
            phone = user_customer.phone,
            postcode = "79332",
            address_line_1 = "38465 Kerluke Tunnel",
            address_line_2 = "Suite 496",
            town_city = "Ocala",
            county = "Cambridgeshire",
            delivery_instr = "Leave at door.",
            is_default = True,
            is_billing_address = True,
            user_id = user_customer.id
        )
        address.save()

        product = ProductModel(
            name="Banana Cake",
            description="Cake made of banana.",
            price=15.5,
            in_stock=True,
            created_by=user.id,
        )
        product.save()

        image = ImageModel(image_URL="./assets/images/products/banana_cake.jpg", product_id=product.id)
        image.save()

        product_2 = ProductModel(
            name = "Refined Metal Soap",
            description= "The beautiful range of Apple Naturalé that has an exciting mix of natural ingredients. With the Goodness of 100% Natural Ingredients",
            price = 366.00,
            in_stock = True,
            created_by = user.id,
        )
        product_2.save()

        image_2 = ImageModel( image_URL = "http://placeimg.com/640/480", product_id=product_2.id)
        image_2.save()

        cart = CartModel(user_id = user.id)
        cart.save()

        cart_item = CartItemModel(product_id= product.id, cart_id = cart.id)
        cart_item.save()

        cart_item_2 = CartItemModel(product_id= product_2.id, cart_id = cart.id, quantity = 3)
        cart_item_2.save()

        order = OrderModel(cart_id=cart.id, user_id= user.id, total = (cart_item.quantity*product.price)+(cart_item_2.quantity*product_2.price) )
        order.save()
        print("Database seeded!")
    except Exception as e:
        print("exception", e)
