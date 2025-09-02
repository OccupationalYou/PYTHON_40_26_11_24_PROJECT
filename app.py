from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import json

import os
from base import SessionLocal, create_db, drop_db

# --- ИМПОРТ ВСЕХ МОДЕЛЕЙ ---
from models.product import Product
from models.user import User

# --- Flask App ---
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_secret")

# --- Flask-Login ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# --- CORS ---
# Позволяет запросы с любого источника (звездочка '*')
CORS(app)


# --- API Routes ---
@app.route("/api/products", methods=["GET"])
def get_products():
    with SessionLocal() as session:
        products = session.query(Product).all()
        # Преобразуем объекты Product в словари для JSON
        products_list = [p.to_dict() for p in products]
        return jsonify(products_list)


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    with SessionLocal() as session:
        product = session.query(Product).filter_by(id=product_id).first()
        if product:
            return jsonify(product.to_dict())
        return jsonify({"error": "Product not found"}), 404


@login_manager.user_loader
def load_user(user_id):
    with SessionLocal() as session:
        return session.get(User, int(user_id))


# --- Routes (existing routes) ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Заповніть усі поля")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)

        with SessionLocal() as session:
            if session.query(User).filter_by(username=username).first():
                flash("Цей користувач вже існує")
                return redirect(url_for("register"))

            new_user = User(username=username, password=hashed_password)
            session.add(new_user)
            session.commit()

        flash("Реєстрація успішна! Увійдіть.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Заповніть усі поля")
            return redirect(url_for("login"))

        with SessionLocal() as session:
            user = session.query(User).filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash("Вхід успішний!")

                next_page = request.args.get('next')
                return redirect(next_page or url_for("index"))
            else:
                flash("Невірні дані для входу")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли з акаунту")
    return redirect(url_for("index"))


# --- Запуск додатку ---
if __name__ == "__main__":
    # create_db()
    app.run(debug=True, port=5000)
