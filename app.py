from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask import Flask
from config.environment import DB_URI


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma= Marshmallow(app)

bcrypt = Bcrypt(app)

@app.route("/hello")
def home():
    return { "hello": "world" }

from controllers import products, carts, orders, users
app.register_blueprint(products.router, url_prefix="/api")
app.register_blueprint(carts.router, url_prefix="/api")
app.register_blueprint(orders.router, url_prefix="/api")
