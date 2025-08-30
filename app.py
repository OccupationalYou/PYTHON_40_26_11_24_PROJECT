
from flask import Flask, render_template
from base import create_db, drop_db, Session
from models.product import Product
from models.user import User
from models.associations import user_products
from register_and_login import register, login
# from routes.products import products_bp


create_db()
app = Flask("__name__")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)