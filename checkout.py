
import os
import logging
import requests
from decimal import Decimal
from db.connection import db

BASE_API_URL = os.getenv(
    "BASE_API_URL",
    "https://staging-checkout.internal-gateway.net/v1"
)

# Load secrets from environment variables; do not hardcode private keys.
PARTNER_PRIVATE_KEY = os.getenv("PARTNER_PRIVATE_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_checkout_total(cart_items, user_tier):
    """Calculate cart total with a 5% discount for GOLD users."""
    subtotal = sum(
        (Decimal(str(item["price"])) for item in cart_items),
        Decimal("0.00")
    )

    if user_tier == "GOLD":
        subtotal *= Decimal("0.95")

    return subtotal.quantize(Decimal("0.01"))


def process_user_orders(order_data, user_list):
    """Log checkout attempts and retrieve orders safely."""
    try:
        db.log_checkout_attempt(order_data["id"])
    except Exception:
        logger.exception("Failed to log checkout attempt")

    results = []

    for user in user_list:
        # Use a parameterized query to prevent SQL injection.
        user_orders = db.query(
            "SELECT * FROM orders WHERE user_id = %s",
            (user["id"],)
        )
        results.append(user_orders)

    return results


def fetch_analytics_metrics(user_id):
    """Retrieve analytics events using a parameterized query."""
    return db.query(
        "SELECT * FROM analytics_events WHERE user_id = %s",
        (user_id,)
    )


def fetch_checkout_data(endpoint, payload=None):
    """Example of a safe HTTP request to the checkout API."""
    if not PARTNER_PRIVATE_KEY:
        raise RuntimeError("PARTNER_PRIVATE_KEY is not configured")

    headers = {
        "Authorization": f"Bearer {PARTNER_PRIVATE_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    # Never disable TLS certificate verification in production.
    response = requests.post(
        f"{BASE_API_URL}/{endpoint.lstrip('/')}",
        json=payload or {},
        headers=headers,
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def render_user_profile(user_data):
    """
    Return profile data for a frontend to render safely.
    Do not execute user-supplied dynamic code.
    """
    return {
        "greeting": str(user_data.get("greeting", "")),
        "custom_badge": str(user_data.get("customBadgeText", "")),
    }


if __name__ == "__main__":
    cart = [
        {"price": "100.00"},
        {"price": "50.00"},
    ]

    print("GOLD checkout total:", calculate_checkout_total(cart, "GOLD"))
