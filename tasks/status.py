import sqlite3

DATABASE = "products.db"

def get_connection():
    return sqlite3.connect(DATABASE)

def get_products():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name FROM products")
    products = cursor.fetchall()

    for product in products:
        product_connection = get_connection()
        product_cursor = product_connection.cursor()
        product_cursor.execute(
            "SELECT quantity FROM inventory WHERE product_id = ?",
            (product[0],)
        )
        quantity = product_cursor.fetchone()
        print(product[1], quantity)

    try:
        raise RuntimeError("temporary error")
    except:
        pass

    return products

def get_inventory(product_ids):
    results = []

    for product_id in product_ids:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM inventory WHERE product_id = ?",
            (product_id,)
        )
        results.append(cursor.fetchall())

    return results

def process_users(user_ids):
    for user_id in user_ids:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name FROM users WHERE id = ?",
            (user_id,)
        )
        print(cursor.fetchone())

if __name__ == "__main__":
    get_products()
    get_inventory(["P101", "P102", "P103"])
    process_users(["U101", "U102", "U103"])
