import sqlite3
import pyodbc


# проверка sql напроса на валидность
def check_sql_string(request):
    invalid = ['=', "'", 'SELECT', 'OR', 'UNION', '--']
    for elem in invalid:
        if elem in request:
            print('ARE YOU HACKER?')
            return False
    return True


def check_sql_list(request):
    for elem in request:
        if not check_sql_string(elem):
            return False
    return True


def for_hacker():
    print('GO AWAY')
    quit()


# коннектимся к базе данных (локальная)
conn = sqlite3.connect('products_bd.sqlite')

cursor = conn.cursor()

# cursor.execute("""CREATE TABLE products
#                   (id INTEGER NOT NULL,
#                   tags TEXT NOT NULL,
#                   product_name TEXT NOT NULL,
#                   product_price INTEGER NOT NULL)""")
# cursor.execute("""CREATE TABLE shopping_list
#                   (product_id INTEGER NOT NULL,
#                   number INTEGER NOT NULL)""")

HELP_MENU = """help : show this message\nadd : add new product
search : search products by tag\nappend : add product to shopping list
new_list : create new shopping list\nshow : show shopping list"""


# функции для работы с базой данных

def create_new_shopping_list():
    # cursor.execute("DELETE FROM shopping_list WHERE '1'='1'")
    # cursor.execute("INSERT INTO shopping_list VALUES ('-1', '-1')")
    cursor.execute("DROP TABLE shopping_list")
    cursor.execute("""CREATE TABLE shopping_list
                      (product_id INTEGER NOT NULL,
                      number INTEGER NOT NULL)""")
    cursor.execute("INSERT INTO shopping_list VALUES ('-1', '-1')")
    conn.commit()


def create_new_products_list():
    # cursor.execute("DELETE FROM shopping_list WHERE '1'='1'")
    # cursor.execute("INSERT INTO shopping_list VALUES ('-1', '-1')")
    cursor.execute("DROP TABLE products")
    cursor.execute("""CREATE TABLE products
                      (id INTEGER NOT NULL,
                      tags TEXT NOT NULL,
                      product_name TEXT NOT NULL,
                      product_price INTEGER NOT NULL)""")
    conn.commit()


def show_shopping_list():
    cursor.execute("SELECT * FROM shopping_list")
    data = cursor.fetchall()
    table = []
    for i in range(1, len(data)):
        id = data[i][0]
        cursor.execute(f"SELECT tags, product_name, product_price FROM products WHERE id='{id}'")
        table.append([data[i][1]] + list(cursor.fetchall()[0]))
    return table


def add_new_product(tags, name, price):
    cursor.execute("SELECT id FROM products")
    id = cursor.fetchall()
    if id == []:
        id = 0
    else:
        id = id[-1][0]
    if check_sql_list(tags) and check_sql_string(name) and check_sql_string(price):
        cursor.execute(
            f"INSERT INTO products VALUES ('{id + 1}', '{';;'.join([str(i) for i in tags])}', '{name}', '{int(price)}')")
    else:
        for_hacker()


def add_to_shopping_list(name):
    if check_sql_string(name):
        cursor.execute(f"SELECT id FROM products WHERE product_name='{name}'")
        product_id = int(cursor.fetchall()[0][0])
        cursor.execute(f"SELECT number FROM shopping_list WHERE product_id='{product_id}'")
        data = cursor.fetchall()
        if data == []:
            cursor.execute(f"INSERT INTO shopping_list VALUES ('{product_id}', '1')")
        else:
            data = data[-1]
            cursor.execute(f"DELETE FROM shopping_list WHERE product_id='{product_id}'")
            cursor.execute(f"INSERT INTO shopping_list VALUES ('{product_id}', '{data[0] + 1}')")
        conn.commit()
    else:
        for_hacker()


def search_by_tag(tag):
    right = []
    cursor.execute(f"SELECT * FROM products")
    results = cursor.fetchall()
    for elem in results:
        if tag.lower() in elem[1]:
            right.append(elem)

    return right