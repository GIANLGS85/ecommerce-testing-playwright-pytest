from playwright.sync_api import Page
from project_locators.components_locators import SearchBarLocators

class SearchBar:

    def __init__(self, page: Page):
        self.page = page
        self.locators = SearchBarLocators(page)

    def search_for(self, term: str):
        """Perform a search."""
        self.locators.search_input.fill(term)
        self.locators.search_button.click()
    
    def clear_search(self):
        """Clear the search input field."""
        self.locators.search_input.clear()
    
    def reset(self):
        """Click reset/clear button to restore default results."""
        self.locators.search_reset.click()
    
    def get_search_term(self) -> str:
        """Get current value in search input."""
        return self.locators.search_input.input_value()
    
    def is_search_empty(self) -> bool:
        """Check if search input is empty."""
        return self.get_search_term() == ""
    
    def search_and_wait(self, term: str, timeout: int = 5000):
        """Search and wait for results to load."""
        self.search_for(term)
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def type_search_term(self, term: str):
        """Type in search box WITHOUT submitting (for autocomplete testing)."""
        self.locators.search_input.fill(term)
    
    def has_suggestions(self) -> bool:
        """Check if search suggestions are visible."""
        return self.locators.search_suggestions.is_visible()
    
    def click_first_suggestion(self):
        """Click first search suggestion."""
        self.locators.search_suggestions.first.click()