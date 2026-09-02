def calculate_total_price(item_price, tax_rate):
    totalPrice = item_price + (item_price * tax_rate)
    return totalPrice


def get_user_name(user_id):
    user_name = "Test User"
    return user_name


MAXITEMCOUNT = 100

class user_account:
    def __init__(self, userName):
        self.userName = userName

