from playwright.sync_api import Page
from project_locators.components_locators import PaginationLocators

class Pagination:

    def __init__(self, page: Page):
        self.page = page
        self.locators = PaginationLocators(page)

    
    def go_to_page(self, page_number: int):
        """Navigate to specific page number."""
        self.page.locator(f'[aria-label="Page-{page_number}"]').click()
    
    def go_to_next_page(self):
        """Go to next page."""
        self.locators.next_button.click()
    
    def go_to_previous_page(self):
        """Go to previous page."""
        self.locators.prev_button.click()
    
    def get_current_page(self) -> int:
        """Get current page number."""
        page_text = self.locators.current_page_indicator.inner_text()
        return int(page_text)
    
    def get_total_pages(self) -> int:
        """Get total number of pages."""
        return self.locators.page_buttons.count()
    
    def is_on_first_page(self) -> bool:
        """Check if currently on first page."""
        return not self.locators.prev_button.is_enabled()
    
    def is_on_last_page(self) -> bool:
        """Check if currently on last page."""
        return not self.locators.next_button.is_enabled()
    
    def is_pagination_visible(self) -> bool:
        """Check if pagination is displayed."""
        return self.locators.pagination_container.is_visible()