"""
BONUS TASK (optional) – API Tests

If you have time remaining after the UI tasks, add 2–3 API test cases here.

Endpoints available:
  GET    /api/products          – list all products
  GET    /api/products/<id>     – single product or 404
  GET    /api/cart              – current cart: {cart, items, total, item_count}
  POST   /api/cart/<id>         – add product to cart; returns updated cart
  DELETE /api/cart/<id>         – remove product from cart; returns updated cart
  POST   /api/checkout          – place order {name, email, address}; 200 or 422

Ideas (pick any):
  - Verify a product response contains expected fields (id, name, price, stock, category)
  - Verify a non-existent product returns 404 with an "error" field
  - Verify adding a product updates item_count and total correctly
  - Verify checkout returns 422 when required fields are missing
  - Verify checkout clears the cart on success
"""
import pytest


pytestmark = pytest.mark.api

 # TODO: add your API tests here
