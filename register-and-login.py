from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from   base import SessionLocal
from models.user import User

app = Flask(__name__)
app.secret_key = "secretkey"  

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Хешуємо пароль
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        with SessionLocal() as db:
            # Перевіряємо, чи вже існує користувач
            if db.query(User).filter_by(username=username).first():
                flash("Цей користувач вже існує")
                return redirect(url_for("register"))

            # Створюємо нового користувача
            new_user = User(username=username, password=hashed_password)
            db.add(new_user)
            db.commit()

        flash("Реєстрація успішна! Увійдіть.")
        return redirect(url_for("login"))

    return render_template("register.html")

