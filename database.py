import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
SALT = "lrhbg28973bf"

def create_db():
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()


    # Создание таблицы user
    sql = """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(256),
            login VARCHAR(256) NOT NULL,
            password VARCHAR(256) NOT NULL,
            birthday DATE,
            bio VARCHAR(256)
        )
    """
    cursor.execute(sql)
    conn.commit()

    sql = """
        CREATE TABLE IF NOT EXISTS wishlists(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title VARCHAR(256),
            comment VARCHAR(256),
            event_date DATE,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
    """
    cursor.execute(sql)
    conn.commit()

    sql = """
        CREATE TABLE IF NOT EXISTS Gifts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wishlist_id INTEGER,
            name VARCHAR(256),
            price INTEGER,
            link VARCHAR(256),
            desire_level INTEGER,
            comment VARCHAR(256),
            FOREIGN KEY (wishlist_id) REFERENCES wishlists(id)
        )
    """
    cursor.execute(sql)
    conn.commit

    sql = """
        CREATE TABLE IN NOT EXISTS Book(
            id INTEGER,
            user_id INTEGER,
            gift_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (gift_id) REFERENCES Gifts(id)
        )
    """

def add_user(login, password):
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password + SALT)

    cursor.execute("INSERT INTO user (login, password) VALUES (?, ?)", (login, hashed_password))

    conn.commit()   

def check_user_exists(login):
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()    

    cursor.execute("SELECT * FROM user WHERE login =?", (login,))

    user = cursor.fetchone() # (...), None
    return True if user else False


def auth_user(login, password):
    # True - фвторизация прошла
    # False - что-то не так


    # 1.
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()    
    cursor.execute("SELECT * FROM user WHERE login = ?", (login,))
    user = cursor.fetchone() # (2, "admin", "йцуйцуцу" | None)
    if not user:
        return -1

    # 2. Сгенерировать хеш пароля "password"
    if check_password_hash(user[2], password+SALT):
        return user[0]
    
    return -1

    # 3. Сравнить сгенерированный хеш с тем, что хранится

    ...


if __name__ == "__main__":
    create_db()