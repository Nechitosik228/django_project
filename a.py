import base64
import hashlib
import requests
import json

url = "https://www.liqpay.ua/api/request"
headers = {
    "Content-Type": "application/json"
}

data = {
    "public_key": "sandbox_4242424242424242",
    "action": "pay",
    "version": 3,
    "amount": 100,
    "currency": "USD",
    "description": "Card Payment",
    "order_id": "123456789",
    "card": "4242424242424242",
    "card_exp_month": "12",
    "card_exp_year": "2025",
    "card_cvv": "123",
    "card_token": "732932398723",  # Use this if paying with a saved card
    "phone": "+548998320",  # Customer's phone number
    "sandbox": "1"  # Enable sandbox mode for testing
}

private_key = "sandbox_4738450943"

# Generate the signature as shown earlier
json_data = json.dumps(data)
signature_string = private_key + json_data + private_key
sha1_hash = hashlib.sha1(signature_string.encode()).digest()
signature = base64.b64encode(sha1_hash).decode()

# Add the signature to the data
data["signature"] = signature

response = requests.post(url, headers=headers, json=data)
print("Response:", response.json())
