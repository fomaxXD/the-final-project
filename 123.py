# Запустите этот скрипт отдельно:
import database
import os

if os.path.exists("wishlist.db"):
    os.remove("wishlist.db")
    print("Старая база удалена")

database.create_db()
print("Новая база создана")