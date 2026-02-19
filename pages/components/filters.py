from playwright.sync_api import Page
from project_locators.components_locators import FilterLocators

class Filters:

    def __init__(self, page: Page):
        self.page = page
        self.locators = FilterLocators(page)

    def filter_by_category(self, category_name: str):
        """Check category filter checkbox."""
        self.page.get_by_label(category_name).check()
    
    def unfilter_by_category(self, category_name: str):
        """Uncheck category filter checkbox."""
        self.page.get_by_label(category_name).uncheck()
    
    def filter_by_brand(self, brand_identifier):
        """
        Filter by brand.
        
        Args:
            brand_identifier: Brand name (str) or index (int)
        """
        if isinstance(brand_identifier, str):
            self.page.get_by_label(brand_identifier).check()
        elif isinstance(brand_identifier, int):
            self.locators.brand_id.nth(brand_identifier).check()
    
    def unfilter_by_brand(self, brand_identifier):
        """
        Remove brand filter.
        
        Args:
            brand_identifier: Brand name (str) or index (int)
        """
        if isinstance(brand_identifier, str):
            self.page.get_by_label(brand_identifier).uncheck()
        elif isinstance(brand_identifier, int):
            self.locators.brand_id.nth(brand_identifier).uncheck()
    
    def set_price_range(self, min_price: None, max_price: None):
        """Set price range filter."""
        if min_price is not None:
            self.locators.price_min.fill(str(min_price))
        if max_price is not None:
            self.locators.price_max.fill(str(max_price))
        self.locators.price_apply_btn.click()
    
    def reset_all_filters(self):
        """Click reset button to clear all filters."""
        self.locators.reset_filters_btn.click()
    
    def reset_all_categories(self):
        """Manually uncheck all category filters."""
        count = self.locators.category_id.count()
        for i in range(count):
            if self.locators.category_id.nth(i).is_checked():
                self.locators.category_id.nth(i).uncheck()
    
    def reset_all_brands(self):
        """Manually uncheck all brand filters."""
        count = self.locators.brand_id.count()
        for i in range(count):
            if self.locators.brand_id.nth(i).is_checked():
                self.locators.brand_id.nth(i).uncheck()
    
    def get_active_filters_count(self) -> int:
        """Get number of active filters."""
        return self.locators.active_filters.count()
    
    def is_filter_applied(self, filter_name: str) -> bool:
        """Check if specific filter is applied."""
        return self.page.get_by_label(filter_name).is_checked()
    
    def get_checked_categories(self) -> list[str]:
        """Get list of checked category names."""
        checked = []
        count = self.locators.category_id.count()
        for i in range(count):
            checkbox = self.locators.category_id.nth(i)
            if checkbox.is_checked():
                label = checkbox.get_attribute("data-test")
                checked.append(label)
        return checked