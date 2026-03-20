import logging

from pages.home_page import HomePage

Logger = logging.getLogger(__name__)

def test_offline_add_item_from_home_to_cart(page, home_page_obj: HomePage):
    """
    Scenario: Add the first available product to the cart and verify visibility.
    """
    # Act: Navigate and add to cart
    # We return a new Page Object from the click action
    home_page_obj.search_and_add_to_cart("Thor Hammer")
    cart_count = home_page_obj.get_cart_count()
    Logger.info(f"Added item to cart, cart count = {cart_count}")

    # Assert: Verification happens on the CartIcon element
    assert cart_count == 1, f"Expected 1 item in cart, but found {cart_count}."