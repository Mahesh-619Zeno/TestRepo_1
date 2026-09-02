def calculate_total_price(item_price, tax_rate):
    if not item_price or not isinstance(item_price, (int, float)) or not tax_rate or not isinstance(tax_rate, (int, float)):
        console.error("Invalid input types for price or tax")
        return 0
    totalPrice = item_price + (item_price * tax_rate)
    return totalPrice


def GetUserName(userId):
    user_name = "Test User"
    return user_name


MAXITEMCOUNT = 100

class user_account:
    def __init__(self, userName):
        self.userName = userName

