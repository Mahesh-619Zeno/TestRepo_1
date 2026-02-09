class PaymentService:
    def process_refund(self, payment_id):
        """
        Misleading: The method name suggests that it processes a refund,
        but it actually charges the user again!
        """
        print(f"Charging customer again for payment ID: {payment_id}")
        self.charge_again(payment_id)

    def charge_again(self, payment_id):
        print(f"[PAYMENT] User charged again for payment {payment_id}")

# Usage
service = PaymentService()
service.process_refund("TXN-8291")  # 🧨 This charges again instead of refunding!
