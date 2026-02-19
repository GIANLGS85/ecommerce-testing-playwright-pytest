from logging import Logger

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.components.project_locators.pages_locators import HomePageLocators
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class HomePage(BasePage):
    """
    HomePage object for e-commerce sites.
    
    Inherits common functionality from BasePage.
    Defines locators and actions specific to home page.
    
    Example:
        home_page = HomePage(page)
        home_page.search_for_product("Thor hammer")
        home_page.signin_link.click()
    """
    
    def __init__(self, page: Page):
        """
        Initialize HomePage.
        
        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        self.locators = HomePageLocators(page)

    # ========================================
    # SORTING METHODS
    # ========================================
    
    def sort_by_option(self, option_value: str):
        """
        Sort products by value.
        
        Args:
            option_value: Sort option value (e.g., "price,asc")
        """
        self.locators.sort_dropdown.select_option(option_value)
        
        # WAIT
        self.wait_for_content_loaded()
    
    def sort_by_label(self, label: str):
        """
        Sort products by label text.
        
        Args:
            label: Sort option label (e.g., "Price (High - Low)")
        """
        self.locators.sort_dropdown.select_option(label=label)
        logger.info(f"Sort product by label <{label}>")
        
        # WAIT
        self.wait_for_content_loaded()
    
    # ========================================
    # PRICE RANGE METHOD
    # ========================================
    
    #def drag_the_slider(self, slider_min: int, slider_max: int):
    #    pass
    
    def set_price_range(self, min_price, max_price):
        """Set price range filter."""
        if min_price is not None:
            self.locators.slider_min = min_price
        if max_price is not None:
            self.locators.slider_max = max_price
    
    # ========================================
    # SEARCH METHODS
    # Create methods for multi-step actions
    # ========================================
    def go_to_cart(self):
        self.locators.cart_icon.click()

    def search_and_add_to_cart(self, keyword: str, quantity: int = 1):
        """
        Searches for a product and adds it to the shopping cart.
        """
        logger.info(f"Searching for product: {keyword}")

        # 1. Search action
        self.locators.search_input.fill(keyword)
        logger.info(f"Searched for product: {keyword}")
        self.locators.search_submit_button.click()
        # 2. Click on the first search result to enter product details
        self.page.locator(f".card-title:text-is('{keyword}')").click()

        logger.info(f"clicked on product: {keyword}")

        # 3. Add to cart (Handling quantity)
        # Note: If a quantity selector exists, it should be handled here.
        # This implementation clicks the add button 'quantity' times for simplicity.
        for _ in range(int(quantity)):
            self.locators.add_to_cart_button.click()

        logger.info(f"Added {quantity} item(s) to cart.")
    
    def search_for_product(self, product_name: str):
        """
        Search for a product.
        
        Multi-step action: fill input + click button.
        Worth creating a method.
        
        Args:
            product_name: Name of product to search for
        """
        self.locators.search_input.fill(product_name)
        self.locators.search_submit_button.click()
        logger.info(f"Searching for product: {product_name}")
        
        # WAIT
        self.wait_for_content_loaded()
    
    def reset_search(self):
        """
        Reset/clear search filters.
        
        Semantic action - worth having a method.
        """
        self.locators.search_reset_button.click()
        logger.info(f"Reset/clear searching")
        
        # WAIT
        self.wait_for_content_loaded()
    
    def search_and_wait(self, product_name: str):
        """
        Search and wait for results to load.
        
        Adds waiting logic - worth having a method.
        
        Args:
            product_name: Name of product to search for
        """
        self.search_for_product(product_name)
        self.wait_for_page_load()
    
    # ========================================
    # FILTER METHODS
    # Dynamic methods that take parameters
    # ========================================
    
    def filter_by_category(self, category_name: str):
        """
        Apply category filter by name.
        
        Args:
            category_name: Category name (e.g., "Hand Tools")
        """
        self.page.get_by_role("checkbox", name=category_name).check()
        logger.info(f"Filter by category <{category_name}> checkbox checked")
        
        # WAIT
        self.wait_for_content_loaded()
    
    def unfilter_by_category(self, category_name: str):
        """
        Remove category filter by name.
        
        Args:
            category_name: Category name (e.g., "Hand Tools")
        """
        self.page.get_by_role("checkbox", name=category_name).uncheck()
        logger.info(f"Filter by category <{category_name}> checkbox unchecked")
        
        # WAIT
        self.wait_for_content_loaded()
    
    def is_category_filtered(self, category_name: str) -> bool:
        """
        Check if category is currently filtered.
        
        Args:
            category_name: Category name to check
            
        Returns:
            True if filtered, False otherwise
        """
        return self.page.get_by_role("checkbox", name=category_name).is_checked()
    
    def filter_by_brand_index(self, brand_index: int):
        """
        Apply brand filter by position.
        
        Use when you don't know brand names.
        
        Args:
            brand_index: Position of brand (0-based)
        """
        self.locators.brand_checkboxes.nth(brand_index).check()
        
        # WAIT
        self.wait_for_content_loaded()
    
    def filter_by_price_range(self, min_price: Optional[float] = None, max_price: Optional[float] = None):
        """
        Filter products by price range.
        
        Multi-step action - worth having a method.
        
        Args:
            min_price: Minimum price (optional)
            max_price: Maximum price (optional)
        """
        if min_price is not None:
            self.locators.price_min_input.fill(str(min_price))
        if max_price is not None:
            self.locators.price_max_input.fill(str(max_price))
        self.locators.price_apply_button.click()
        
        # WAIT
        self.wait_for_content_loaded()
    
    def reset_all_filters(self):
        """
        Reset all filters to default.
        
        Click reset button if available.
        """
        self.locators.reset_filters_button.click()
        
        # WAIT
        self.wait_for_content_loaded()
    
    
    # ========================================
    # PAGINATION METHODS
    # ========================================
    
    def go_to_page(self, page_number: int):
        """
        Navigate to specific page number.
        
        Args:
            page_number: Page number to navigate to
        """
        self.page.locator(f'[aria-label="Page-{page_number}"]').click()
        
        # WAIT
        self.wait_for_content_loaded()
    
    def go_to_next_page(self):
        """Go to next page of results."""
        self.locators.next_page_button.click()
        
        # WAIT
        self.wait_for_content_loaded()
    
    def go_to_previous_page(self):
        """Go to previous page of results."""
        self.locators.prev_page_button.click()
        
        # WAIT
        self.wait_for_content_loaded()

    def navigate_to_cart(self):
        """Navigates to the checkout page from the cart icon."""
        self.locators.cart_icon.click()
        expect(self.locators.cart_icon).to_be_visible()
        self.locators.cart_icon.click()
    
    # ========================================
    # GETTER METHODS
    # Return processed data
    # ========================================
    
    def click_first_product(self):
        """Click the first product."""
        self.locators.product_cards.first.click()
    
    def get_product_count(self) -> int:
        """
        Get number of visible products.
        
        Returns:
            Number of product cards on page
        """
        return self.get_element_count(self.locators.product_cards)
    
    def get_all_product_names(self) -> list[str]:
        """
        Get all visible product names.
        
        Returns:
            List of product names
        """
        all_product_names = self.locators.product_name.all_inner_texts()
        logger.info(f"Get all visible product names: {all_product_names}")
        return all_product_names
    
    def get_all_product_prices(self) -> list[float]:
        """
        Get all visible product prices as floats.
        
        Processes price strings to remove currency symbols.
        
        Returns:
            List of prices as floats
        """
        price_texts = self.locators.product_prices.all_inner_texts()
        list_of_product_prices = [float(p.replace("$", "").replace(",", "").strip()) for p in price_texts]
        logger.info(f"This is the list_of_product_prices: {list_of_product_prices}")
        return list_of_product_prices
    
    def get_cart_count(self) -> int:
        """
        Get number of items in cart from badge.
        
        Returns:
            Number of items in cart
        """
        count_text = self.locators.cart_count_badge.inner_text()
        return int(count_text) if count_text else 0
    
    def wait_for_products_to_load(self, expected_count: int = 9):
        """
        Wait for products to load.
        
        PRO approach: Uses Playwright's smart waiting.
        
        Args:
            expected_count: Expected number of products (default: 9)
        """
        expect(self.locators.product_cards).to_have_count(expected_count, timeout=10000)
    
    # ========================================
    # VERIFICATION METHODS
    # Complex checks
    # ========================================
    
    def is_products_sorted_by_price_ascending(self) -> bool:
        """
        Verify products are sorted by price (low to high).
        
        Returns:
            True if sorted correctly, False otherwise
        """
        prices = self.get_all_product_prices()
        return prices == sorted(prices)
    
    def is_products_sorted_by_price_descending(self) -> bool:
        """
        Verify products are sorted by price (high to low).
        
        Returns:
            True if sorted correctly, False otherwise
        """
        prices = self.get_all_product_prices()
        return prices == sorted(prices, reverse=True)
    
    def is_products_sorted_by_name_ascending(self) -> bool:
        """
        Verify products are sorted by name (A-Z).
        
        Returns:
            True if sorted correctly, False otherwise
        """
        names = self.get_all_product_names()
        return names == sorted(names)

