from playwright.sync_api import Page
from project_locators.components_locators import ProductGridLocators

class ProductGrid:

    def __init__(self, page: Page):
        self.page = page
        self.locators = ProductGridLocators(page)

    def get_product_count(self) -> int:
        """Get number of visible products."""
        return self.locators.product_cards.count()
    
    def click_product(self, index: int = 0):
        """Click a product by index (0-based)."""
        self.locators.product_cards.nth(index).click()
    
    def click_first_product(self):
        """Click the first product."""
        self.locators.product_cards.first.click()
    
    def click_last_product(self):
        """Click the last product."""
        self.locators.product_cards.last.click()
    
    def get_all_product_names(self) -> list[str]:
        """Get all visible product names."""
        return self.locators.product_names.all_inner_texts()
    
    def get_all_product_prices(self) -> list[float]:
        """Get all visible product prices as floats."""
        price_texts = self.locators.product_prices.all_inner_texts()
        return [float(p.replace("$", "").replace(",", "").strip()) for p in price_texts]
    
    def get_product_name(self, index: int = 0) -> str:
        """Get name of specific product."""
        return self.locators.product_names.nth(index).inner_text()
    
    def get_product_price(self, index: int = 0) -> float:
        """Get price of specific product."""
        price_text = self.locators.product_prices.nth(index).inner_text()
        return float(price_text.replace("$", "").replace(",", "").strip())
    
    def is_product_visible(self, index: int = 0) -> bool:
        """Check if product at index is visible."""
        return self.locators.product_cards.nth(index).is_visible()
    
    def wait_for_products(self, timeout: int = 5000):
        """Wait for products to load."""
        self.locators.product_cards.first.wait_for(state="visible", timeout=timeout)
    
    def has_products(self) -> bool:
        """Check if any products are displayed."""
        return self.get_product_count() > 0
    
    def has_no_results_message(self) -> bool:
        """Check if 'no results' message is visible."""
        return self.no_results_message.is_visible()
    
    def sort_by(self, option: str):
        """Sort products by option (e.g., 'Price (High - Low)')."""
        self.locators.sort_dropdown.select_option(label=option)
    
    def get_current_sort_option(self) -> str:
        """Get currently selected sort option."""
        return self.locators.sort_dropdown.input_value()
    
    def is_sorted_by_price_ascending(self) -> bool:
        """Verify products are sorted by price (low to high)."""
        prices = self.get_all_product_prices()
        return prices == sorted(prices)
    
    def is_sorted_by_price_descending(self) -> bool:
        """Verify products are sorted by price (high to low)."""
        prices = self.get_all_product_prices()
        return prices == sorted(prices, reverse=True)
    
    def is_sorted_by_name_ascending(self) -> bool:
        """Verify products are sorted by name (A-Z)."""
        names = self.get_all_product_names()
        return names == sorted(names)