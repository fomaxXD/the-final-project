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
            booked INTEGER DEFAULT 0,
            FOREIGN KEY (wishlist_id) REFERENCES wishlists(id)
        )
    """
    cursor.execute(sql)
    conn.commit()

    sql = """
        CREATE TABLE IF NOT EXISTS Book(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            gift_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (gift_id) REFERENCES Gifts(id)
        )
    """
    cursor.execute(sql)
    conn.commit()

def add_user(login, password, email, birthday, bio):
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password + SALT)

    cursor.execute("INSERT INTO user (login, password, email, birthday, bio) VALUES (?, ?, ?, ?, ?)", (login, hashed_password, email, birthday, bio))
    conn.commit()   

def check_user_exists(login):
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()    

    cursor.execute("SELECT * FROM user WHERE login =?", (login,))

    user = cursor.fetchone()
    return True if user else False


def auth_user(login, password):
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()    
    cursor.execute("SELECT * FROM user WHERE login = ?", (login,))
    user = cursor.fetchone()
    if not user:
        return -1

    if check_password_hash(user[3], password+SALT):
        return user[0]

def cr_wishlist(user_id, title, comment, date):
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()    
    cursor.execute(
        "INSERT INTO wishlists (user_id, title, comment, event_date) VALUES (?, ?, ?, ?)",
        (user_id, title, comment, date)
    )
    conn.commit()
    wishlist_id = cursor.lastrowid
    conn.close()
    return wishlist_id


def get_user_wishlists(user_id):
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM wishlists WHERE user_id = ?", (user_id,))
    wishlists = cursor.fetchall()
    conn.close() 
    return wishlists

def get_wishlist_by_id(wishlist_id):
    conn = sqlite3.connect("wishlist.db")
    cursor  = conn.cursor()

    cursor.execute("SELECT * FROM wishlists WHERE id = ?", (wishlist_id,))
    wishlist = cursor.fetchone()
    conn.close() 
    return wishlist


def get_gifts_by_wishlist(wishlist_id):
    conn = sqlite3.connect("wishlist.db")
    cursor  = conn.cursor()

    cursor.execute("SELECT * FROM Gifts WHERE wishlist_id = ?", (wishlist_id,))
    gifts = cursor.fetchall()
    conn.close()
    return gifts

def add_gift(wishlist_id, name, price, link, desire_level, comment):
    conn = sqlite3.connect("wishlist.db")
    cursor  = conn.cursor()

    cursor.execute(
        "INSERT INTO Gifts (wishlist_id, name, price, link, desire_level, comment, booked) VALUES (?, ?, ?, ?, ?, ?, ?)", (wishlist_id, name, price, link, desire_level, comment, 0)
    )
    conn.commit()
    gift_id = cursor.lastrowid
    conn.close() 
    return gift_id

def change_gift_status(gift_id):
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE Gifts SET booked = 1 - booked WHERE id = ?", (gift_id,))
    conn.commit()
    conn.close()
    
def update_user_login(user_id, new_login):
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE user SET login = ? WHERE id = ?", (new_login, user_id))
    conn.commit()
    conn.close()

def update_user_bio(user_id, new_bio):
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE user SET bio = ? WHERE id = ?", (new_bio, user_id))
    conn.commit()
    conn.close()

def update_user_birthday(user_id, new_birthday):
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE user SET birthday = ? WHERE id = ?", (new_birthday, user_id))
    conn.commit()
    conn.close()

def get_user_info(user_id):
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()

    cursor.execute("SELECT login, birthday, bio FROM user WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_profile(user_id):
    conn = sqlite3.connect("wishlist.db")
    cursor = conn.cursor()
    cursor.execute("SELECT login, birthday, bio FROM user WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM wishlists WHERE user_id = ?", (user_id,))
    wishlists_count = cursor.fetchone()[0]
    conn.close()
    return {
        'login': user[0] if user else None,
        'birthday': user[1] if user else None,
        'bio': user[2] if user else None,
        'wishlists_count': wishlists_count
    }


    
if __name__ == "__main__":
    create_db()
