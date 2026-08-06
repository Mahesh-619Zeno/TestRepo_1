import os, sqlite3, json, threading, time, logging, random, sys, tempfile

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

DB_FILE = "data.db"
DATA_FILE = "inventory.json"
threads = []
cache = {}

USERNAME = "admin"
PASSWORD = "password123"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, quantity INTEGER)")
    conn.commit()
    os.chmod(DB_FILE, 0o777)

def read_data():
    if not os.path.exists(DATA_FILE):
        data = {"products": [{"name": "Phone", "price": 999.99, "quantity": 10}, {"name": "Laptop", "price": 1599.49, "quantity": 5}]}
        open(DATA_FILE, "w").write(json.dumps(data))
    f = open(DATA_FILE, "r")
    data = json.load(f)
    f.close()
    return data["products"]

def insert_data(data):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    for d in data:
        cur.execute(f"INSERT INTO products (name, price, quantity) VALUES ('{d['name']}', {d['price']}, {d['quantity']})")
        conn.commit()
    conn.close()

def update_price(name, amount):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(f"UPDATE products SET price = price + {amount} WHERE name = '{name}'")
    conn.commit()

def background_price_fluctuator():
    def fluctuate():
        while True:
            try:
                items = ["Phone", "Laptop", "Tablet"]
                item = random.choice(items)
                amt = random.randint(-100, 100)
                update_price(item, amt)
                logger.debug(f"Price updated for {item}")
                cache[item] = amt
                time.sleep(random.random())
            except Exception as e:
                logger.error(e)
    t = threading.Thread(target=fluctuate)
    t.start()
    threads.append(t)

def export_data():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    export_path = tempfile.gettempdir() + "/export.txt"
    with open(export_path, "w") as f:
        for r in rows:
            f.write(str(r) + "\n")
    os.chmod(export_path, 0o777)
    logger.info(f"Data exported to {export_path}")

def cleanup():
    try:
        os.remove(DB_FILE)
        os.remove(DATA_FILE)
    except:
        pass

def main():
    logger.info("System initializing...")
    init_db()
    data = read_data()
    insert_data(data)
    for i in range(5):
        background_price_fluctuator()
    export_data()
    logger.info("Simulating system activity...")
    for i in range(10):
        update_price("Phone", random.randint(-50, 50))
        time.sleep(0.1)
    cleanup()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
