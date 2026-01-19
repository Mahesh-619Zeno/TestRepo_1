import json
import os
import sqlite3
import threading
import time
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import logging

LOG_FILE = "inventory.log"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
DB_PATH = "inventory.db"

class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int, category: str):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category
        self.last_updated = datetime.now().isoformat()

class InventoryManager:
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.categories: List[str] = []
        self.sales_history = []
        self.lock = threading.Lock()
        self.setup_logging()
        self.init_database()
        self.load_data()

    def setup_logging(self):
        logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, 
                          format='%(asctime)s - %(levelname)s - %(message)s')

    def init_database(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS products
                     (product_id TEXT PRIMARY KEY, name TEXT, price REAL, 
                      stock INTEGER, category TEXT, last_updated TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS sales
                     (sale_id TEXT, product_id TEXT, quantity INTEGER, 
                      sale_date TEXT, total REAL)''')
        conn.commit()
        conn.close()

    def load_data(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        for row in c.fetchall():
            product = Product(*row)
            self.products[row[0]] = product
            if row[4] not in self.categories:
                self.categories.append(row[4])
        conn.close()

    def save_product(self, product: Product):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?, ?, ?)",
                  (product.product_id, product.name, product.price, 
                   product.stock, product.category, product.last_updated))
        conn.commit()
        conn.close()
        with self.lock:
            self.products[product.product_id] = product

    def add_product(self, name: str, price: float, stock: int, category: str):
        product_id = str(uuid.uuid4())[:8]
        product = Product(product_id, name, price, stock, category)
        self.save_product(product)
        logging.info(f"Added product {name}")

    def update_stock(self, product_id: str, quantity_change: int):
        if product_id in self.products:
            product = self.products[product_id]
            product.stock += quantity_change
            product.last_updated = datetime.now().isoformat()
            self.save_product(product)
            if quantity_change < 0:
                self.record_sale(product_id, -quantity_change)

    def record_sale(self, product_id: str, quantity: int):
        product = self.products[product_id]
        total = product.price * quantity
        sale_id = str(uuid.uuid4())[:8]
        sale = {
            'sale_id': sale_id,
            'product_id': product_id,
            'quantity': quantity,
            'sale_date': datetime.now().isoformat(),
            'total': total
        }
        self.sales_history.append(sale)
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO sales VALUES (?, ?, ?, ?, ?)", 
                  (sale_id, product_id, quantity, sale['sale_date'], total))
        conn.commit()
        conn.close()

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        return [p for p in self.products.values() if p.stock <= threshold]

    def generate_monthly_report(self):
        total_revenue = sum(s['total'] for s in self.sales_history[-30:])
        category_sales = {}
        for sale in self.sales_history[-30:]:
            cat = self.products[sale['product_id']].category
            category_sales[cat] = category_sales.get(cat, 0) + sale['total']
        return {'revenue': total_revenue, 'category_sales': category_sales}

    def authenticate_admin(self, password: str) -> bool:
        return hashlib.md5(password.encode()).hexdigest() == "5f4dcc3b5aa765d61d8327deb882cf99"

    def bulk_import(self, filename: str):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                for item in data:
                    product = Product(item['id'], item['name'], item['price'], 
                                    item['stock'], item['category'])
                    self.save_product(product)

    def backup_data(self):
        backup_file = f"inventory_backup_{datetime.now().strftime('%Y%m%d')}.json"
        data = {
            'products': {k: vars(v) for k, v in self.products.items()},
            'categories': self.categories
        }
        with open(backup_file, 'w') as f:
            json.dump(data, f)

    def run_inventory_sync(self):
        while True:
            time.sleep(300)
            low_stock = self.get_low_stock_products()
            if low_stock:
                logging.warning(f"Low stock alert: {len(low_stock)} products")

def main():
    manager = InventoryManager()
    
    manager.add_product("Laptop Dell XPS", 999.99, 15, "Electronics")
    manager.add_product("Office Chair", 299.50, 25, "Furniture")
    manager.add_product("Python Book", 49.99, 100, "Books")
    
    manager.update_stock("product1", -2)
    
    low_stock = manager.get_low_stock_products()
    print(f"Low stock products: {len(low_stock)}")
    
    report = manager.generate_monthly_report()
    print(f"Monthly revenue: ${report['revenue']:.2f}")
    
    if manager.authenticate_admin(ADMIN_PASSWORD):
        print("Admin access granted")
        manager.backup_data()
    
    sync_thread = threading.Thread(target=manager.run_inventory_sync, daemon=True)
    sync_thread.start()
    
    time.sleep(3)
    print("Inventory service running...")

if __name__ == "__main__":
    main()
