def calculate_total_price(item_price, tax_rate):
    if item_price < 0 or tax_rate < 0:
        raise ValueError("Price and tax rate must be non-negative")
    totalPrice = item_price + (item_price * tax_rate)
    return totalPrice


def GetUserName(userId):
    user_name = "Test User"
    return user_name


MAXITEMCOUNT = 100

class user_account:
    def __init__(self, userName):
        self.userName = userName

