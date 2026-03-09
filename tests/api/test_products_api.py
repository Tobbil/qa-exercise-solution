"""
EXISTING TESTS – Products API
These tests are provided as examples. Do not modify them.
"""
import pytest


pytestmark = [
    pytest.mark.api,
    pytest.mark.smoke
]


def test_get_all_products_returns_200(api_client):
    session, base_url = api_client
    response = session.get(f'{base_url}/api/products')
    assert response.status_code == 200

def test_get_all_products_returns_list(api_client):
    session, base_url = api_client
    response = session.get(f'{base_url}/api/products')
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
