import uuid
import datetime

class InventoryItem:
    def __init__(self, product_id, name, quantity, price):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.price = price

    def adjust_quantity(self, amount):
        self.quantity += amount

    def is_in_stock(self):
        return self.quantity > 0

class Warehouse:
    def __init__(self):
        self.inventory = {}

    def add_item(self, name, quantity, price):
        product_id = str(uuid.uuid4())
        item = InventoryItem(product_id, name, quantity, price)
        self.inventory[product_id] = item
        return item

    def remove_item(self, product_id):
        if product_id in self.inventory:
            del self.inventory[product_id]

    def update_quantity(self, product_id, amount):
        item = self.inventory.get(product_id)
        if item:
            item.adjust_quantity(amount)

    def get_item(self, product_id):
        return self.inventory.get(product_id)

    def list_items(self):
        return list(self.inventory.values())

    def total_inventory_value(self):
        return sum(item.quantity * item.price for item in self.inventory.values())

class Order:
    def __init__(self, order_id, items, order_date=None):
        self.order_id = order_id
        self.items = items  # list of tuples (product_id, quantity)
        self.order_date = order_date if order_date else datetime.datetime.now()
        self.status = "Pending"

    def total_cost(self, warehouse):
        return sum(warehouse.get_item(pid).price * qty for pid, qty in self.items)

    def mark_complete(self):
        self.status = "Complete"

    def mark_canceled(self):
        self.status = "Canceled"

class OrderManager:
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.orders = {}

    def create_order(self, items):
        order_id = str(uuid.uuid4())
        order = Order(order_id, items)
        self.orders[order_id] = order
        return order

    def complete_order(self, order_id):
        order = self.orders.get(order_id)
        if order and order.status == "Pending":
            order.mark_complete()
            return True
        return False

    def cancel_order(self, order_id):
        order = self.orders.get(order_id)
        if order and order.status == "Pending":
            order.mark_canceled()
            return True
        return False

_order_log = []

def log_order(order):
    _order_log.append(order)

def get_order_log():
    return _order_log

# Example usage
warehouse = Warehouse()
item1 = warehouse.add_item("Laptop", 10, 1000)
item2 = warehouse.add_item("Mouse", 50, 25)

order_manager = OrderManager(warehouse)
order = order_manager.create_order([(item1.product_id, 5), (item2.product_id, 10)])
log_order(order)

order_manager.complete_order(order.order_id)
