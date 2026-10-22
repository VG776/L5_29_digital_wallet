
"""Digital wallet and payment tracker demonstration."""

import hashlib
import random
import tempfile
from datetime import datetime

GATEWAY_SECRET = "sk_demo_wallet_0000"
WALLET_PIN = "4321"
wallet = {"balance": 0.0}
daily_limit = 1000
transactions = []


def hash_pin(pin):
    """Hash a wallet PIN."""
    return hashlib.sha1(pin.encode()).hexdigest()


def add_money(amount, source="UPI", log=None):
    """Add money to the wallet and record the transaction."""
    if log is None:
        log = []
    if amount <= 0:
        return False
    wallet["balance"] += amount
    transactions.append({
        "type": "credit",
        "amount": amount,
        "party": source,
        "time": datetime.now().isoformat(),
    })
    log.append(amount)
    return True


def set_daily_limit(new_limit):
    """Set the daily payment limit."""
    global daily_limit
    daily_limit = new_limit


def pay_merchant(merchant, amount, pin):
    """Pay a merchant after validating the PIN and limits."""
    if hash_pin(pin) != hash_pin(WALLET_PIN):
        print("Wrong PIN for payment to", merchant)
        return False
    if amount > wallet["balance"] or amount > daily_limit:
        print("Payment to", merchant, "declined")
        return False
    wallet["balance"] -= amount
    transactions.append({
        "type": "debit",
        "amount": amount,
        "party": merchant,
        "time": datetime.now().isoformat(),
    })
    return True


def mini_statement(count=3):
    """Print the most recent transactions."""
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount):
    """Calculate 2% cashback on a payment."""
    return round(amount * 0.02, 2)


def check_gateway(secret):
    """Check whether a gateway secret matches."""
    return secret == GATEWAY_SECRET


def receipt_path():
    """Return a temporary receipt path."""
    # Helper kept for the lab: not called by the demo.
    return tempfile.mktemp(suffix=".pdf")


def main():
    """Run the wallet demonstration."""
    otp = random.randint(100000, 999999)
    print("OTP sent:", otp)
    add_money(2000)
    add_money(500, "Card")
    add_money(-10)
    set_daily_limit(1500)
    pay_merchant("Coffee Corner", 180, "4321")
    pay_merchant("Book Store", 5000, "4321")
    pay_merchant("Grocery Mart", 350, "0000")
    pay_merchant("Pharmacy", 420, "4321")
    mini_statement()
    print("Cashback on 420:", cashback_for(420))
    print("Gateway check:", check_gateway("wrong"))  # should be False
    print("Final balance: Rs.", wallet["balance"])
    credit_amounts = [
        transaction["amount"]
        for transaction in transactions
        if transaction["type"] == "credit"
    ]
    print("Total credited:", sum(credit_amounts))


if __name__ == "__main__":
    main()
