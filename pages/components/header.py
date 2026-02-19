from playwright.sync_api import Page
from project_locators.components_locators import HeaderLocators

class Header:

    def __init__(self, page: Page):
        self.page = page
        self.locators = HeaderLocators(page)

    def click_logo(self):
        """Click logo to return home."""
        self.locators.logo.click()
    
    def navigate_to_category(self, category_name: str):
        """Navigate to category by name."""
        self.page.get_by_role("link", name=category_name).click()
    
    def open_cart(self):
        """Click cart icon."""
        self.locators.cart_icon.click()
    
    def open_user_menu(self):
        """Open user dropdown menu."""
        self.locators.user_menu.click()
    
    def get_cart_count(self) -> int:
        """Get number of items in cart from badge."""
        count_text = self.locators.cart_count_badge.inner_text()
        return int(count_text) if count_text else 0
    
    def is_user_logged_in(self) -> bool:
        """Check if user is logged in."""
        return self.locators.logout_button.is_visible()
    
    def click_login(self):
        """Click login/sign in link."""
        self.locators.login_link.click()
    
    def logout(self):
        """Click logout button."""
        self.open_user_menu()
        self.locators.logout_button.click()
    
    def get_all_category_names(self) -> list[str]:
        """Get all category names from navigation."""
        return self.locators.category_links.all_inner_texts()