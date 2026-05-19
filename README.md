# the-final-project
# Список референсов
https://followish.io

# Что пользователь может делать на веб-приложении
Авторизация
На главное странице кнопка "создать вишлист". Если пользователь не входил в аккаунт, то его перекинет на авторизацию.
После авторизации есть 3 страницы на выбор:
1. моя страница. Там можно создать вишлист и отслеживать его
2. Подарки друзьям. Что пользователь дарил своим друзьям
3. Настройки. Личные данные(Смена имя, дня рождения, описания о себе), Безопаность и вход(Смена почты, пароля, удаление аккаунта), Выйти из профиля
В моей странице будет кнопка "создать вишлист". Перейдя по ней будет страница с создание самого вишлиста(название, комментарий, дата, сохранить). После "сохранить" в "моей станице"появится отдельный вишлист. Внутри есть кнопка "Добавить подарок"(Ссылка на товар, !!название!!, цена , степень желанности подарка, комментарий, сохранить)

# Страница регистрации/входа пользователя:
Регистрация: 1. Почта 2. Имя, пароль
Вход: 1. Почта 2. Пароль



Это БД для сайта
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


