import sqlite3


def initiate_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            price FLOAT
         )
    ''')
    connection.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INT NOT NULL,
            balance INT NOT NULL         
         )
    ''')
    connection.commit()
    connection.close()


def add_product(title, description, price):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products WHERE title=?', (title,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO Products (title, description, price) VALUES (?,?,?)',
                       (title, description, price))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
    if cursor.fetchone() is not None:
        connection.commit()
        connection.close()
        return True
    else:
        connection.commit()
        connection.close()
        return False


def add_user(username, email, age):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)',
                   (username, email, age, 1000))

    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products')
    product_list = cursor.fetchall()

    connection.commit()
    connection.close()
    return product_list
