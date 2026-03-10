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


def test_get_product_returns_expected_fields(api_client):
    session, base_url = api_client
    response = session.get(f"{base_url}/api/products/1")
    data = response.json()
    assert response.status_code == 200
    assert "id" in data
    assert "name" in data
    assert "price" in data
    assert "stock" in data
    assert "category" in data


def test_get_nonexistent_product_returns_404_and_error(api_client):
    session, base_url = api_client
    response = session.get(f"{base_url}/api/products/99999999")
    data = response.json()
    assert response.status_code == 404
    assert "error" in data


def test_checkout_missing_fields_returns_422_and_error(api_client):
    session, base_url = api_client
    session.post(f"{base_url}/api/cart/1")
    cart_response = session.get(f"{base_url}/api/cart")
    data = cart_response.json()
    assert cart_response.status_code == 200
    assert data["item_count"] == 1

    response = session.post(f"{base_url}/api/checkout", json={})
    data = response.json()
    assert response.status_code == 422
    assert "error" in data


def test_checkout_clears_cart_on_success(api_client):
    session, base_url = api_client
    session.post(f"{base_url}/api/cart/1")
    cart_response = session.get(f"{base_url}/api/cart")
    data = cart_response.json()
    assert cart_response.status_code == 200
    assert data["item_count"] == 1

    checkout_data = {
        "name": "Test User",
        "email": "test@example.com",
        "address": "123 Test St"
    }
    response = session.post(f"{base_url}/api/checkout", json=checkout_data)
    assert response.status_code == 200

    cart_response = session.get(f"{base_url}/api/cart")
    data = cart_response.json()
    assert cart_response.status_code == 200
    assert data["item_count"] == 0
