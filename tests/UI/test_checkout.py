import pytest
import logging

from config.config import Config
from conftest import browser
from pages.cart_page import CartPage
from pages.home_page import HomePage
from utils.data_loader import get_csv_data

# 1. Load external test data (SKU, Quantity, Expected Price)
# CSV content format: product_name, qty, expected_price
TEST_DATA = get_csv_data("test_orders.csv")

logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("setup_session")
@pytest.mark.parametrize("data", TEST_DATA)
def test_checkout_process(authenticated_page, data):
    """
    Test the checkout process (uses 'authenticated_page' fixture for automatic login)
    """
    # Arrange (Setup data)
    product_name = data['product_name']
    quantity = int(data['quantity'])
    expected_price = float(data['expected_price'])

    # Act (Execute actions)
    # 1. Search and add item to cart
    home_page = HomePage(authenticated_page)
    logger.info(f"Authenticated. now searching for product: {product_name}")
    home_page.search_and_add_to_cart(product_name, quantity)
    home_page.go_to_cart()

    # 2. Proceed to checkout
    checkout_page = CartPage(authenticated_page)
    #
    # 3. Retrieve final price
    actual_price = checkout_page.get_final_price()

    # Assert (Verify results)
    logger.info(f"Verifying price: Expected {expected_price}, Got {actual_price}")

    assert actual_price == expected_price, \
        f"❌ Price mismatch! Expected: {expected_price}, Actual: {actual_price}"
    checkout_page.proceed_to_checkout()