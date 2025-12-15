import uuid
import datetime

class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def adjust_stock(self, quantity):
        self.stock += quantity

    def is_available(self, quantity):
        return self.stock >= quantity

class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def get_total_spent(self):
        return sum(order.total_amount() for order in self.orders)

class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def item_total(self):
        return self.product.price * self.quantity

class Order:
    def __init__(self, order_id, customer, items, date=None):
        self.order_id = order_id
        self.customer = customer
        self.items = items
        self.date = date if date else datetime.datetime.now()
        self.status = "Pending"

    def total_amount(self):
        return sum(item.item_total() for item in self.items)

    def mark_shipped(self):
        self.status = "Shipped"

    def mark_cancelled(self):
        self.status = "Cancelled"

class Store:
    def __init__(self):
        self.products = {}
        self.customers = {}
        self.orders = {}

    def add_product(self, name, price, stock):
        product_id = str(uuid.uuid4())
        product = Product(product_id, name, price, stock)
        self.products[product_id] = product
        return product

    def register_customer(self, name, email):
        customer_id = str(uuid.uuid4())
        customer = Customer(customer_id, name, email)
        self.customers[customer_id] = customer
        return customer

    def place_order(self, customer_id, items_info):
        if customer_id not in self.customers:
            return None

        order_items = []
        for product_id, quantity in items_info:
            product = self.products.get(product_id)
            if not product or not product.is_available(quantity):
                return None
            order_items.append(OrderItem(product, quantity))
        order_id = str(uuid.uuid4())
        order = Order(order_id, self.customers[customer_id], order_items)
        self.orders[order_id] = order
        self.customers[customer_id].add_order(order)
        for item in order_items:
            item.product.adjust_stock(-item.quantity)
        return order

    def get_customer_orders(self, customer_id):
        customer = self.customers.get(customer_id)
        if customer:
            return customer.orders
        return []

    def restock_product(self, product_id, quantity):
        if product_id in self.products:
            self.products[product_id].adjust_stock(quantity)

    def cancel_order(self, order_id):
        order = self.orders.get(order_id)
        if order and order.status == "Pending":
            order.mark_cancelled()
            for item in order.items:
                item.product.adjust_stock(item.quantity)
            return True
        return False

    def get_order(self, order_id):
        return self.orders.get(order_id)

    def get_products_below_stock(self, threshold):
        return [p for p in self.products.values() if p.stock < threshold]

    def summary(self):
        total_orders = len(self.orders)
        total_customers = len(self.customers)
        sales = sum(order.total_amount() for order in self.orders.values())
        return {
            "total_orders": total_orders,
            "total_customers": total_customers,
            "total_sales": sales,
        }

# Example usage
store = Store()
prod1 = store.add_product("Book", 10.99, 50)
prod2 = store.add_product("Pen", 1.19, 200)
prod3 = store.add_product("Headphones", 29.99, 30)

cust1 = store.register_customer("Alice", "alice@email.com")
cust2 = store.register_customer("Bob", "bob@email.com")

order1 = store.place_order(cust1.customer_id, [(prod1.product_id, 2), (prod2.product_id, 5)])
order2 = store.place_order(cust2.customer_id, [(prod2.product_id, 10), (prod3.product_id, 1)])

restock_needed = store.get_products_below_stock(40)
summary = store.summary()

order1.mark_shipped()
store.cancel_order(order2.order_id)
