from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import database

app = Flask(__name__)
app.secret_key = "alekrmqkmwemk"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register_page():
    if request.method == "GET":
        return render_template("register.html")
    else:
        login = request.form['login']
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']
        email = request.form['email']
        birthday = request.form['birthday']
        bio = request.form['bio']
        errors = []


        # Проверка на существующего пользователя
        if  database.check_user_exists(login):
            errors.append("Такой пользователь уже существует")


        # Проверка на одинаковые пароли
        if pass1 != pass2:
            errors.append("Пароли не совпадают")


        # Проверка на качество пароля
        if len(pass1) <  8:
            errors.append("Длина пароля должна быть больше 8 символов")


        # Проверка на регистрацию
        if len(errors) == 0:
            # Регистрация
            database.add_user(login, pass1)
            return render_template("success_register.html")


        else:
            return render_template("register.html", errors=errors)

@app.route("/login", methods=["POST", "GET"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")
    else:
        login = request.form["login"]
        password = request.form["password"]
        user_id = database.auth_user(login, password)


        if user_id:
            print("Успешный вход")
            session["user_id"] = user_id
            session["login"] = login
            return redirect(url_for("index"))
        else:
            print("Что-то не так")
            return render_template("login.html", errors=["Неверный логин или пароль"])

@app.route("/success_register")
def success_register():
    return render_template("success_register.html")

@app.route("/choice")
def choice():
    return render_template("choice.html")

@app.route("/my_page")
def my_page():
    return render_template("my_page.html")

@app.route("/gifts_for_friends")
def gifts_for_friends():
    return render_template("gifts_for_friends.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/create_wishlist")
def create_wishlist():
    return render_template("create_wishlist.html")

app.run(debug=True)