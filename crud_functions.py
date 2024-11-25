import sqlite3

initiate_db = sqlite3.connect('telegram.db')
cursor = initiate_db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL

)
''')


# cursor.execute("SELECT COUNT (*) FROM Products")                                   #общее количество записей
# get_all_products = cursor.fetchone()[0]
# print(get_all_products)

get_all_products = [("Продукт 1", "Описание 1", 100), ("Продукт 2", "Описание 2", 200), ("Продукт 3", "Описание 3", 300),("Продукт 4", "Описание 4", 400)]
cursor.executemany("INSERT INTO Products (title, description, price) VALUES (?,?,?)", get_all_products)

cursor.execute("SELECT title, description, price FROM Products WHERE id=1")
title1, description1, price1 = cursor.fetchone()

cursor.execute("SELECT title, description, price FROM Products WHERE id=2")
title2, description2, price2 = cursor.fetchone()

cursor.execute("SELECT title, description, price FROM Products WHERE id=3")
title3, description3, price3 = cursor.fetchone()

cursor.execute("SELECT title, description, price FROM Products WHERE id=4")
title4, description4, price4 = cursor.fetchone()

initiate_db.commit()