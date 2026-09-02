def calculate_total_price(item_price, tax_rate):
    totalPrice = round(item_price + (item_price * tax_rate), 2)
    return totalPrice


def GetUserName(userId):
    user_name = "Test User"
    return user_name


MAXITEMCOUNT = 100

class user_account:
    def __init__(self, userName):
        self.userName = userName

