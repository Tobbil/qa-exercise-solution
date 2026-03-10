"""
CANDIDATE TASK – Add your new tests here.

Context:
  ShopEasy is a simple e-commerce app running locally at http://localhost:5050
  The app has: a product listing page, product detail pages, a cart, checkout,
  and a confirmation page.

Your tasks:
  1. Write tests for the 3 scenarios described in the README (Scenarios A, B, C).
  2. Refactor the flawed test below (see the comment).
  3. Leave a short comment at the bottom of this file explaining what else you
     would test if you had more time.

You may use the existing tests in test_product_listing.py as reference for how
fixtures and the driver work.
"""

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

pytestmark = pytest.mark.ui


PRODUCT_NAME_CLASS = "product-name"
PRODUCT_PRICE_CLASS = "product-price"
PRODUCT_STOCK_CLASS = "product-stock"
PRODUCT_CARD_CLASS = "product-card"
CART_ITEM_CLASS = "cart-item"
LOGO_CLASS = "logo"
DATA_PRODUCT_ID_ATTR = "data-product-id"
ADD_TO_CART_BTN = "add-to-cart-btn"
CART_TOTAL_ID = "cart-total"
CHECKOUT_BTN_ID = "checkout-btn"
INPUT_NAME_ID = "input-name"
INPUT_EMAIL_ID = "input-email"
INPUT_ADDRESS_ID = "input-address"
PLACE_ORDER_BTN_ID = "place-order-btn"
ERROR_MESSAGE_ID = "error-message"


def parse_price(price_text: str) -> float:
    """Convert a price string like '$19.99' to a float 19.99."""
    return float(price_text.replace("$", "").strip())


def get_in_stock_products(product_cards):
    """Filter the list of product card elements to only those that are in stock."""
    return [
        card
        for card in product_cards
        if "in stock"
        in card.find_element(By.CLASS_NAME, PRODUCT_STOCK_CLASS).text.lower()
    ]


def add_product_to_cart(driver, product_id):
    """Click the 'Add to Cart' button for the product with the given ID."""
    button_locator = (
        By.CSS_SELECTOR,
        f".{PRODUCT_CARD_CLASS}[{DATA_PRODUCT_ID_ATTR}='{product_id}'] .{ADD_TO_CART_BTN}",
    )
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button_locator)).click()


# -----------------------------------------------------------------------
# TASK 2: Refactor this test. It works, but has quality problems.
#         Fix it without changing what is being tested.
# -----------------------------------------------------------------------
def test_add_to_cart_bad(driver, app_server):
    driver.get(app_server)
    product_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, PRODUCT_CARD_CLASS))
    )
    assert product_cards, "No products found on the listing page"

    first_product = product_cards[0]
    first_product_id = first_product.get_attribute(DATA_PRODUCT_ID_ATTR)
    add_product_to_cart(driver, first_product_id)
    WebDriverWait(driver, 10).until(EC.url_contains("/cart"))
    assert (
        "/cart" in driver.current_url
    ), f"Expected to be on cart page after adding product, but URL is {driver.current_url}"


# -----------------------------------------------------------------------
# TASK 1: Write your 3 new test cases below
# -----------------------------------------------------------------------


# Scenario A: Product detail page
# When a user clicks on a product name, they should land on the product detail page.
# The detail page should show the product name, price, and stock status.
def test_product_detail_page(driver, app_server):
    driver.get(app_server)
    product_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, PRODUCT_CARD_CLASS))
    )
    assert product_cards, "No products found on the listing page"

    first_product = product_cards[0]

    expected_product_name = first_product.find_element(
        By.CLASS_NAME, PRODUCT_NAME_CLASS
    ).text
    expected_product_price = first_product.find_element(
        By.CLASS_NAME, PRODUCT_PRICE_CLASS
    ).text
    expected_product_stock = first_product.find_element(
        By.CLASS_NAME, PRODUCT_STOCK_CLASS
    ).text
    product_id = first_product.get_attribute(DATA_PRODUCT_ID_ATTR)

    first_product.find_element(By.CLASS_NAME, PRODUCT_NAME_CLASS).click()
    WebDriverWait(driver, 10).until(EC.url_contains(f"/product/{product_id}"))
    assert driver.current_url.endswith(
        f"/product/{product_id}"
    ), f"Expected URL to end with /product/{product_id} but got {driver.current_url}"

    product_name_product_page = (
        WebDriverWait(driver, 10)
        .until(EC.presence_of_element_located((By.CLASS_NAME, PRODUCT_NAME_CLASS)))
        .text
    )
    product_price_product_page = (
        WebDriverWait(driver, 10)
        .until(EC.presence_of_element_located((By.CLASS_NAME, PRODUCT_PRICE_CLASS)))
        .text
    )
    product_stock_product_page = (
        WebDriverWait(driver, 10)
        .until(EC.presence_of_element_located((By.CLASS_NAME, PRODUCT_STOCK_CLASS)))
        .text
    )

    assert (
        product_name_product_page == expected_product_name
    ), f"Expected product name '{expected_product_name}' but got '{product_name_product_page}'"
    assert (
        product_price_product_page == expected_product_price
    ), f"Expected product price '{expected_product_price}' but got '{product_price_product_page}'"
    assert (
        expected_product_stock.lower() in product_stock_product_page.lower()
    ), f"Expected product stock '{expected_product_stock}' but got '{product_stock_product_page}'"


# Scenario B: Cart total calculation
# When a user adds multiple products to the cart, the displayed total
# should equal the sum of each product's price.
def test_cart_total_calculation(driver, app_server):
    driver.get(app_server)

    product_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, PRODUCT_CARD_CLASS))
    )

    in_stock_products = get_in_stock_products(product_cards)
    assert (
        len(in_stock_products) >= 2
    ), "Need at least 2 in-stock products to test cart total calculation"

    first_product, second_product = in_stock_products[:2]

    first_product_id = first_product.get_attribute(DATA_PRODUCT_ID_ATTR)
    second_product_id = second_product.get_attribute(DATA_PRODUCT_ID_ATTR)

    first_price = parse_price(
        first_product.find_element(By.CLASS_NAME, PRODUCT_PRICE_CLASS).text
    )
    second_price = parse_price(
        second_product.find_element(By.CLASS_NAME, PRODUCT_PRICE_CLASS).text
    )
    expected_total = first_price + second_price

    add_product_to_cart(driver, first_product_id)
    WebDriverWait(driver, 10).until(EC.url_contains("/cart"))
    assert (
        "/cart" in driver.current_url
    ), f"Expected to be on cart page after adding product, but URL is {driver.current_url}"

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, LOGO_CLASS))
    ).click()

    add_product_to_cart(driver, second_product_id)
    WebDriverWait(driver, 10).until(EC.url_contains("/cart"))
    assert (
        "/cart" in driver.current_url
    ), f"Expected to be on cart page after adding product, but URL is {driver.current_url}"

    cart_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, CART_ITEM_CLASS))
    )
    assert (
        len(cart_items) == 2
    ), f"Expected 2 items in the cart but found {len(cart_items)}"

    cart_total = parse_price(
        WebDriverWait(driver, 10)
        .until(EC.presence_of_element_located((By.ID, CART_TOTAL_ID)))
        .text.replace("Total:", "")
    )

    assert cart_total == pytest.approx(
        expected_total
    ), f"Expected cart total to be ${expected_total:.2f} but got ${cart_total:.2f}"


# Scenario C: Checkout form validation
# When a user submits the checkout form with missing required fields,
# an error message should be displayed and the order should NOT be confirmed.
@pytest.mark.parametrize(
    "name, email, address",
    [
        ("", "test@example.com", "123 Test St"),
        ("Tester McTest", "test@example.com", ""),
        ("", "test@example.com", ""),
    ],
)
def test_checkout_form_validation(driver, app_server, name, email, address):
    driver.get(app_server)
    product_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, PRODUCT_CARD_CLASS))
    )
    assert product_cards, "No products found on the listing page"
    first_product = product_cards[0]
    first_product_id = first_product.get_attribute(DATA_PRODUCT_ID_ATTR)

    add_product_to_cart(driver, first_product_id)
    WebDriverWait(driver, 10).until(EC.url_contains("/cart"))
    assert (
        "/cart" in driver.current_url
    ), f"Expected to be on cart page after adding product, but URL is {driver.current_url}"

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, CHECKOUT_BTN_ID))
    ).click()
    WebDriverWait(driver, 10).until(EC.url_contains("/checkout"))
    assert (
        "/checkout" in driver.current_url
    ), f"Expected to be on checkout page after clicking checkout, but URL is {driver.current_url}"

    name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, INPUT_NAME_ID))
    )
    name_input.clear()
    name_input.send_keys(name)

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, INPUT_EMAIL_ID))
    )
    email_input.clear()
    email_input.send_keys(email)

    address_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, INPUT_ADDRESS_ID))
    )
    address_input.clear()
    address_input.send_keys(address)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, PLACE_ORDER_BTN_ID))
    ).click()

    error_message = (
        WebDriverWait(driver, 10)
        .until(EC.visibility_of_element_located((By.ID, ERROR_MESSAGE_ID)))
        .text
    )
    assert (
        error_message
    ), "Expected an error message to be displayed for invalid form submission"

    assert driver.current_url.endswith(
        "/checkout"
    ), f"Expected to remain on checkout after invalid form submission, but URL is {driver.current_url}"


# -----------------------------------------------------------------------
# TASK 3: Leave your note here
# -----------------------------------------------------------------------
# What else would you test if you had more time?
# (A few bullet points is all we need.)

# - Adding out-of-stock products to cart
# - Removing products from cart
# - Cart persistence after page reload
# - Checkout happy path (successful order creation)
# - Checkout behavior when cart is empty
# - Navigating directly to /product/{id} for non-existent product
