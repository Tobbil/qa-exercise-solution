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


# -----------------------------------------------------------------------
# TASK 2: Refactor this test. It works, but has quality problems.
#         Fix it without changing what is being tested.
# -----------------------------------------------------------------------
@pytest.mark.ui
def test_add_to_cart_bad(driver, app_server):
    import time
    driver.get('http://localhost:5050')
    time.sleep(3)
    btns = driver.find_elements(By.CLASS_NAME, 'add-to-cart-btn')
    btns[0].click()
    time.sleep(3)
    assert 'Cart' in driver.title


# -----------------------------------------------------------------------
# TASK 1: Write your 3 new test cases below
# -----------------------------------------------------------------------

# Scenario A: Product detail page
# When a user clicks on a product name, they should land on the product detail page.
# The detail page should show the product name, price, and stock status.
@pytest.mark.ui
def test_product_detail_page(driver, app_server):
    pass  # TODO: implement


# Scenario B: Cart total calculation
# When a user adds multiple products to the cart, the displayed total
# should equal the sum of each product's price.
@pytest.mark.ui
def test_cart_total_calculation(driver, app_server):
    pass  # TODO: implement


# Scenario C: Checkout form validation
# When a user submits the checkout form with missing required fields,
# an error message should be displayed and the order should NOT be confirmed.
@pytest.mark.ui
def test_checkout_form_validation(driver, app_server):
    pass  # TODO: implement


# -----------------------------------------------------------------------
# TASK 3: Leave your note here
# -----------------------------------------------------------------------
# What else would you test if you had more time?
# (A few bullet points is all we need.)
