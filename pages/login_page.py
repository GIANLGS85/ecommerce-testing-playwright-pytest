from playwright.sync_api import Page, expect
from pages.components.project_locators.pages_locators import LoginPageLocators
from pages.base_page import BasePage
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class LoginPage(BasePage):

    def __init__(self, page: Page):
        """
        Initialize LoginPage.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        self.locators = LoginPageLocators(page)

    def launch_login_page(self):
        """Navigate to login page."""
        logger.info(f"Navigating to login page: {Config.LOGIN_URL}")
        self.page.goto(Config.LOGIN_URL)

    def login(self, email: str, password: str):
        """Perform login."""
        logger.info(f"Logging in as: {email}")
        self.locators.email_input.fill(email)
        self.locators.password_input.fill(password)
        self.locators.login_button_text.click()

        # Optional: wait for navigation or dashboard
        self.page.wait_for_load_state("networkidle")

