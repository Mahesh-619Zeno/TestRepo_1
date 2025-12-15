from datetime import datetime
import json
import uuid

class Product:
    def __init__(self, product_id, name, price, stock, category, description):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category
        self.description = description

class Catalog:
    def __init__(self, storage_file='catalog.json'):
        self.products = {}
        self.storage_file = storage_file
        self.load_catalog()

    def add_product(self, name, price, stock, category, description):
        product_id = str(uuid.uuid4())
        product = Product(product_id, name, price, stock, category, description)
        self.products[product_id] = product
        self.save_catalog()
        return product

    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            self.save_catalog()

    def update_stock(self, product_id, amount):
        product = self.products.get(product_id)
        if product:
            product.stock = amount
            self.save_catalog()

    def list_products(self):
        return list(self.products.values())

    def save_catalog(self):
        data = {}
        for pid, prod in self.products.items():
            data[pid] = {
                "name": prod.name,
                "price": prod.price,
                "stock": prod.stock,
                "category": prod.category,
                "description": prod.description
            }
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load_catalog(self):
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                for pid, p in data.items():
                    self.products[pid] = Product(pid, p['name'], p['price'], p['stock'], p['category'], p['description'])
        except FileNotFoundError:
            self.products = {}

class User:
    def __init__(self, user_id, username, role='customer'):
        self.user_id = user_id
        self.username = username
        self.role = role

class Order:
    def __init__(self, order_id, user, items, created_at=None):
        self.order_id = order_id
        self.user = user
        self.items = items  # dict product_id -> quantity
        self.created_at = created_at if created_at else datetime.now()
        self.status = "Pending"

    def total(self, catalog):
        total_price = 0
        for pid, qty in self.items.items():
            product = catalog.products.get(pid)
            if product:
                total_price += product.price * qty
        return total_price

    def update_status(self, new_status):
        valid_status = ["Pending", "Cancelled", "Shipped", "Delivered"]
        if new_status in valid_status:
            self.status = new_status

class OrderManager:
    def __init__(self, catalog):
        self.orders = {}
        self.catalog = catalog

    def place_order(self, user, items):
        order_id = str(uuid.uuid4())
        # Missing checks for stock availability before placing order or updating stock
        order = Order(order_id, user, items)
        self.orders[order_id] = order
        return order

    def cancel_order(self, order_id):
        order = self.orders.get(order_id)
        if order and order.status == "Pending":
            order.update_status("Cancelled")
            return True
        return False

    def ship_order(self, order_id):
        order = self.orders.get(order_id)
        if order and order.status == "Pending":
            order.update_status("Shipped")
            return True
        return False

# Example usage
catalog = Catalog()
product1 = catalog.add_product("Smartphone", 699.99, 50, "Electronics", "Latest model smartphone")
product2 = catalog.add_product("Earphones", 29.99, 150, "Accessories", "Wireless earphones")

user1 = User("u001", "alice")
order_manager = OrderManager(catalog)
order = order_manager.place_order(user1, {product1.product_id: 2, product2.product_id: 1})
order_manager.ship_order(order.order_id)
