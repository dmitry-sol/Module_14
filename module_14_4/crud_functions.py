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


def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products')
    product_list = cursor.fetchall()

    connection.commit()
    connection.close()

    return product_list
