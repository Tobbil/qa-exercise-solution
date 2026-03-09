"""
EXISTING TESTS – Product Listing Page
These tests are provided as examples. Do not modify them.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


pytestmark = [
    pytest.mark.ui,
    pytest.mark.smoke
]


def test_page_loads_with_products(driver, app_server):
    driver.get(app_server)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'product-card'))
    )
    product_cards = driver.find_elements(By.CLASS_NAME, 'product-card')
    assert len(product_cards) > 0, 'No product cards found on the home page'


def test_product_name_is_visible(driver, app_server):
    driver.get(app_server)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'product-name'))
    )
    names = driver.find_elements(By.CLASS_NAME, 'product-name')
    assert len(names) > 0
    assert names[0].text != ''


def test_product_has_price(driver, app_server):
    driver.get(app_server)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'product-price'))
    )
    prices = driver.find_elements(By.CLASS_NAME, 'product-price')
    assert len(prices) > 0
    for price in prices:
        assert '$' in price.text, f'Price missing $ symbol: {price.text}'
