from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.components.project_locators.pages_locators import CartPageLocators
import logging

logger = logging.getLogger(__name__)

class CartPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = CartPageLocators(page)

    def get_product_row(self, product_name: str):
        """Returns the specific table row for a given product name."""
        return self.page.locator("tr").filter(has_text=product_name)


    def get_total_cart_amount(self) -> float:
        """Extracts the final total price as a float."""
        total_text = self.locators.total_price.inner_text()
        return float(total_text.replace('$', '').strip())

    def get_cart_total(self) -> int:
        """Retrieves the final amount from the checkout page."""
        expect(self.locators.total_price_text).to_be_visible()
        price_str = self.locators.total_price_text.text_content()
        clean_price = price_str.replace("$", "").replace(",", "").strip()
        return int(clean_price)

    def get_final_price(self) -> int:
        """Retrieves the final amount from the checkout page."""
        expect(self.locators.total_price_text).to_be_visible()
        price_str = self.locators.total_price_text.text_content()
        clean_price = price_str.replace("$", "").replace(",", "").strip()
        return float(clean_price)

    def proceed_to_checkout(self) -> None:
        """Proceeds to the checkout page."""
        self.locators.checkout_button.click()

