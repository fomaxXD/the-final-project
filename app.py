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
            database.add_user(login, pass1, email, birthday, bio)
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
            return redirect(url_for("success_login"))
        else:
            print("Что-то не так")
            return render_template("login.html", errors=["Неверный логин или пароль"])

@app.route("/success_register")
def success_register():
    return render_template("success_register.html")

@app.route("/success_login")
def success_login():
    login = session.get("login")
    return render_template("success_login.html", login=login)

@app.route("/choice")
def choice():
    login = session.get("login")
    return render_template("choice.html", login=login)

@app.route("/gifts_for_friends")
def gifts_for_friends():
    return render_template("gifts_for_friends.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/my_page")
def my_page():
    user_id = session.get("user_id")
    login = session.get("login")
    if not user_id:
        return redirect(url_for("login_page"))
    wishlists = database.get_user_wishlists(user_id)
    return render_template("my_page.html", wishlists=wishlists, login=login)

@app.route("/create_wishlist", methods=['GET', 'POST'])
def create_wishlist():
    
    if request.method == "GET":
        return render_template("create_wishlist.html")
    
    user_id = session.get("user_id")
    title = request.form.get("title", "")
    comment = request.form.get("comment", "")
    date = request.form.get("date", "")
    
    print("user_id:", user_id)
    print("title:", title)
    print("comment:", comment)
    print("date:", date)
    
    if not user_id:
        return redirect(url_for("login_page"))
    
    if not title:
        return render_template("create_wishlist.html", errors=["Название обязательно"])
    
    wishlist_id = database.cr_wishlist(user_id, title, comment, date)
    print("wishlist_id:", wishlist_id)
    
    if wishlist_id:
        return redirect(url_for("my_page"))
    else:
        return render_template("create_wishlist.html", errors=["Ошибка создания вишлиста"])



@app.route("/list_gifts/<int:wishlist_id>")
def list_gifts(wishlist_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login_page"))
    
    wishlist = database.get_wishlist_by_id(wishlist_id)
    

    if not wishlist or wishlist[1] != user_id:
        return redirect(url_for("my_page"))
    
    gifts = database.get_gifts_by_wishlist(wishlist_id)
    return render_template("list_gifts.html", wishlist=wishlist, gifts=gifts)

@app.route("/add_gifts/<int:wishlist_id>", methods=['GET', 'POST'])
def add_gifts(wishlist_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login_page"))
    
    wishlist = database.get_wishlist_by_id(wishlist_id)
    if not wishlist or wishlist[1] != user_id:
        return redirect(url_for("my_page"))
    
    if request.method == "GET":
        return render_template("add_gifts.html", wishlist_id=wishlist_id, wishlist=wishlist)
    else:
        name = request.form['name']
        price = request.form['price']
        link = request.form['link']
        desire_level = request.form['desire_level']
        comment = request.form['comment']
        
        gift_id = database.add_gift(wishlist_id, name, price, link, desire_level, comment)
        
        if gift_id:
            return redirect(url_for('list_gifts', wishlist_id=wishlist_id))
        else:
            return render_template("add_gift.html", wishlist_id=wishlist_id, wishlist=wishlist, errors=["Ошибка добавления подарка"])
        
@app.route("/toggle_booked/<int:gift_id>/<int:wishlist_id>")
def change_gift_status(gift_id, wishlist_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login_page"))
    
    wishlist = database.get_wishlist_by_id(wishlist_id)
    if not wishlist or wishlist[1] != user_id:
        return redirect(url_for("my_page"))
    
    database.change_gift_status(gift_id)
    return redirect(url_for("list_gifts", wishlist_id=wishlist_id))
        

        
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


app.run(debug=True)