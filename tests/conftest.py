import os
import random
import pytest
from playwright.sync_api import Page
# from pytest_playwright.pytest_playwright import page
from config.config import Config
from utils.api_client import APIClient
from utils.helpers import Helpers
from pages.login_page import LoginPage
from pages.home_page import HomePage

# ============================================================================
# USER PAGE FIXTURE
# ============================================================================

AUTH_FILE = "playwright/.auth/user.json"
TEST_USER =  Config.TEST_USER
TEST_PWD =  Config.TEST_PWD

#
# @pytest.fixture(scope="function", autouse=False)
# def setup_auth(browser: Browser):
#     login_page = browser.new_page()
#     login_page.goto(Config.LOGIN_URL)
#     login_page.locator('[data-test="email"]').fill(Config.TEST_USER)
#     login_page.locator('[data-test="password"]').fill(Config.TEST_PWD)
#     login_page.locator('[data-test="login-submit"]').click()
#     expect(login_page.locator('[data-test="page-title"]')).to_have_text("My account")
#     #expect(login_page.get_by_label("Page context").locator("span")).to_have_text("My Account")
#     # Save the auth file after succesfully login
#     login_page.context.storage_state(path=AUTH_FILE)
#     login_page.close()
#     yield
#     os.remove(AUTH_FILE)
#
# # Load auth file and return logged-in page
# @pytest.fixture
# def user_page(browser: Browser):
#     context = browser.new_context(storage_state=AUTH_FILE)
#     page = context.new_page()
#     yield page #return the logged page
#     context.close()
# ============================================================================

# ============================================================================
# AUTHENTICATION PAGE FIXTURE
# ============================================================================
@pytest.fixture()
def delete_store_state():
    """Delete storage state file before tests to ensure clean state."""
    if os.path.exists(AUTH_FILE):
        os.remove(AUTH_FILE)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    if os.path.exists(AUTH_FILE):
        return {
            **browser_context_args,
            "storage_state": AUTH_FILE,
            "viewport": {"width": 1280, "height": 800},
        }
    return {**browser_context_args, "viewport": {"width": 1280, "height": 800}}

@pytest.fixture(scope="session", autouse=False)
def setup_session(browser):
    """Login una volta e salva lo storage state."""
    if os.path.exists(AUTH_FILE): os.remove(AUTH_FILE)
    if not os.path.exists(AUTH_FILE):
        context = browser.new_context()
        page = context.new_page()

        login_page = LoginPage(page)

        page.goto(Config.LOGIN_URL)

        with page.expect_navigation():
            login_page.login(TEST_USER, TEST_PWD)

        page.wait_for_load_state("networkidle")

        context.storage_state(path=AUTH_FILE)
        context.close()

@pytest.fixture(scope="function")
def authenticated_page(page):
    page.goto(Config.BASE_URL)
    return page

# ============================================================================

@pytest.fixture
def api_client(playwright):
    # Create the request context manually
    request_context = playwright.request.new_context()
    client = APIClient(request_context)
    yield client
    # Clean up the context after the test
    request_context.dispose()

@pytest.fixture
def utils():
    return Helpers()
#
# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args):
#     """
#     Configures the browser context (e.g., viewport size, locale).
#     """
#     return {
#         **browser_context_args,
#         "viewport": {"width": 1280, "height": 800},
#         "locale": "en-US"  # setting to en-US for international compatibility
#     }
#

@pytest.fixture
def home_page_obj(page: Page) -> HomePage:
    """
    Provides HomePage instance with automatic navigation.

    Usage:
        def test_homepage(home_page: HomePage):
            home_page.search_for_product("hammer")
            assert home_page.get_product_count() > 0
    """
    home_page_obj = HomePage(page)
    page.goto(Config.BASE_URL)

    return home_page_obj

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """LoginPage instance"""
    return LoginPage(page)



#============================================================================
# AUTHENTICATION FIXTURES
# ============================================================================

@pytest.fixture
def valid_user() -> dict:
    """
    Returns valid user credentials from config.

    Usage:
        def test_login(login_page: LoginPage, valid_user: dict):
            login_page.login(valid_user["email"], valid_user["password"])
    """
    return {
        "email": Config.TEST_USER,
        "password": Config.TEST_PWD
    }


@pytest.fixture
def invalid_user() -> dict:
    """
    Returns invalid credentials for negative tests.

    Usage:
        def test_invalid_login(login_page: LoginPage, invalid_user: dict):
            login_page.login(invalid_user["email"], invalid_user["password"])
            login_page.verify_error_message()
    """
    return {
        "email": "invalid@example.com",
        "password": "wrongpassword"
    }

#============================================================================
#TEST DATA FIXTURES
#============================================================================

@pytest.fixture
def valid_contact_data() -> dict:
    """Valid data for contact form submission"""
    return {
        "name": "John Doe",
        "email": f"contact_{random.randint(1000, 9999)}@example.com",
        "subject": "Test Inquiry",
        "message": "This is a test message for automated testing."
    }


@pytest.fixture
def test_product() -> dict:
    """Test product data for e-commerce tests"""
    return {
        "id": "PROD-001",
        "name": "Test Product",
        "price": 29.99,
        "quantity": 2
    }


@pytest.fixture
def checkout_data() -> dict:
    """Valid checkout/payment data"""
    return {
        "billing_address": "123 Test Street",
        "city": "Test City",
        "state": "CA",
        "zip": "12345",
        "card_number": "4111111111111111",  # Test card
        "cvv": "123",
        "expiry": "12/25"
    }


# ============================================================================
# HELPER FIXTURES
# ============================================================================

@pytest.fixture
def wait_for_animation(page: Page):
    """
    Provides a function to wait for CSS animations.

    Usage:
        def test_modal(home_page: HomePage, wait_for_animation):
            home_page.open_modal_button.click()
            wait_for_animation(500)  # Wait 500ms
            expect(home_page.modal).to_be_visible()
    """

    def wait(milliseconds: int = 300):
        page.wait_for_timeout(milliseconds)
    return wait


# ============================================================================
# PARAMETRIZED TEST DATA
# ============================================================================

@pytest.fixture(params=["hammer", "screwdriver", "pliers"])
def search_term(request):
    """
    Provides multiple search terms for parametrized tests.
    Test runs once for each parameter.

    Usage:
        def test_search_products(home_page: HomePage, search_term: str):
            # This test runs 3 times (hammer, screwdriver, pliers)
            home_page.search_for_product(search_term)
            assert home_page.get_product_count() > 0
    """
    return request.param
