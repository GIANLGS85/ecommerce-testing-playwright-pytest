import os
import random
import time
import pytest
import logging
from playwright.sync_api import Page
from playwright_stealth import stealth  # Cloudflare bypass: stealth mode
from config.config import Config
from utils.api_client import APIClient
from utils.helpers import Helpers
from utils.cloudflare_helper import CloudflareHelper  # Cloudflare bypass: helper
from pages.login_page import LoginPage
from pages.home_page import HomePage

logger = logging.getLogger(__name__)

# ============================================================================
# USER PAGE FIXTURE
# ============================================================================

AUTH_FILE = "playwright/.auth/user.json"
TEST_USER =  Config.TEST_USER
TEST_PWD =  Config.TEST_PWD


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
    """
    Login once and save storage state for session reuse.

    🚀 ENHANCED WITH CLOUDFLARE BYPASS:
    Strategy:
    1. Use cloudscraper to bypass Cloudflare JS Challenge
    2. Extract clearance cookies
    3. Inject into Playwright context
    4. Apply stealth mode to hide Playwright
    5. Perform login
    6. Save storage state for subsequent tests

    Cleanup resources properly:
    - Close page BEFORE context
    - Handle errors gracefully with logging
    """
    is_ci = os.getenv("CI") == "true"
    logger.info(f"Setup session: CI_MODE={'✓ CI' if is_ci else '✗ Local'}")

    # Delete existing auth file to ensure clean state
    if os.path.exists(AUTH_FILE):
        os.remove(AUTH_FILE)
        logger.info(f"Deleted stale auth file: {AUTH_FILE}")

    context = None
    page = None
    cf_cookies = None

    try:
        if not os.path.exists(AUTH_FILE):
            logger.info("\n" + "="*70)
            logger.info("🔐 SESSION SETUP - STARTING")
            logger.info("="*70)

            # =====================================================================
            # STEP 1: BYPASS CLOUDFLARE WITH CLOUDSCRAPER
            # =====================================================================
            logger.info("\n📌 STEP 1: Cloudflare Bypass with cloudscraper")
            logger.info("-" * 70)

            try:
                cf_cookies = CloudflareHelper.get_cloudflare_cookies(
                    Config.BASE_URL,
                    timeout=30
                )
                logger.info("✅ Cloudflare bypass successful!")

            except Exception as cf_error:
                logger.warning(f"⚠️  Cloudflare bypass failed: {cf_error}")
                logger.warning("   Continuing without pre-bypass (will rely on stealth mode)...")
                cf_cookies = {}

            # =====================================================================
            # STEP 2: CREATE CONTEXT WITH REALISTIC SETTINGS
            # =====================================================================
            logger.info("\n📌 STEP 2: Create Playwright context")
            logger.info("-" * 70)

            context = browser.new_context(
                # Realistic user-agent to avoid suspicion
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                ignore_https_errors=True,
                viewport={"width": 1280, "height": 800},
            )
            logger.info("✓ Context created")

            page = context.new_page()
            logger.info("✓ Page created")

            # =====================================================================
            # STEP 3: INJECT CLOUDFLARE COOKIES (if obtained)
            # =====================================================================
            if cf_cookies:
                logger.info("\n📌 STEP 3: Inject Cloudflare clearance cookies")
                logger.info("-" * 70)

                try:
                    CloudflareHelper.inject_cookies_to_context(
                        context,
                        cf_cookies,
                        "practicesoftwaretesting.com"
                    )
                    logger.info("✓ Cloudflare cookies injected")

                except Exception as inject_error:
                    logger.warning(f"⚠️  Failed to inject cookies: {inject_error}")

            # =====================================================================
            # STEP 4: APPLY STEALTH MODE
            # =====================================================================
            logger.info("\n📌 STEP 4: Apply Playwright stealth mode")
            logger.info("-" * 70)
            
            try:
                stealth(page)
                logger.info("✓ Stealth mode applied (hides Playwright from bot detection)")
                
            except Exception as stealth_error:
                logger.warning(f"⚠️  Stealth mode failed: {stealth_error}")

            # =====================================================================
            # STEP 5: SET TIMEOUTS FOR CLOUDFLARE
            # =====================================================================
            logger.info("\n📌 STEP 5: Configure Cloudflare timeouts")
            logger.info("-" * 70)

            timeout_ms = Config.CLOUDFLARE_TIMEOUT
            page.set_default_timeout(timeout_ms)
            logger.info(f"✓ Timeout set to {timeout_ms}ms ({timeout_ms/1000}s)")

            # =====================================================================
            # STEP 6: NAVIGATE AND LOGIN
            # =====================================================================
            logger.info("\n📌 STEP 6: Navigate to login page")
            logger.info("-" * 70)

            logger.info(f"→ Navigating to: {Config.LOGIN_URL}")
            page.goto(Config.LOGIN_URL)
            logger.info("✓ Navigation started")

            # Wait for page to be interactive
            try:
                page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)
                logger.info("✓ DOM content loaded")
            except Exception as e:
                logger.warning(f"⚠️  DOM load timeout: {e}")

            # Additional wait for Cloudflare resolution
            page.wait_for_timeout(2000)
            logger.info("✓ Cloudflare resolution wait complete")

            # =====================================================================
            # STEP 7: PERFORM LOGIN
            # =====================================================================
            logger.info("\n📌 STEP 7: Perform login")
            logger.info("-" * 70)

            login_page = LoginPage(page)
            logger.info(f"→ Logging in as: {TEST_USER}")

            try:
                with page.expect_navigation():
                    login_page.login(TEST_USER, TEST_PWD)
                logger.info("✓ Login submitted, navigation started")

            except Exception as login_error:
                logger.error(f"❌ Login error: {login_error}")
                raise

            # =====================================================================
            # STEP 8: WAIT FOR PAGE LOAD
            # =====================================================================
            logger.info("\n📌 STEP 8: Wait for page load after login")
            logger.info("-" * 70)

            try:
                page.wait_for_load_state("networkidle", timeout=timeout_ms)
                logger.info("✓ Page loaded (networkidle)")
            except Exception as e:
                logger.warning(f"⚠️  Network idle timeout: {e}")
                # Continue anyway - page might be loaded
                page.wait_for_timeout(3000)
                logger.info("✓ Fallback wait complete")

            # =====================================================================
            # STEP 9: SAVE STORAGE STATE
            # =====================================================================
            logger.info("\n📌 STEP 9: Save storage state")
            logger.info("-" * 70)

            try:
                context.storage_state(path=AUTH_FILE)
                logger.info(f"✓ Storage state saved: {AUTH_FILE}")
            except Exception as save_error:
                logger.error(f"❌ Failed to save storage state: {save_error}")
                raise

            logger.info("\n" + "="*70)
            logger.info("✅ SESSION SETUP - COMPLETE")
            logger.info("="*70 + "\n")

    except Exception as e:
        logger.error("\n" + "="*70)
        logger.error("❌ SESSION SETUP - FAILED")
        logger.error(f"Error: {str(e)}")
        logger.error("="*70 + "\n")
        # Don't re-raise - let tests continue (they might skip auth)

    finally:
        # =====================================================================
        # CLEANUP: Close resources in correct order
        # =====================================================================
        logger.info("Cleaning up resources...")

        if page is not None:
            try:
                page.close()
                logger.info("✓ Page closed")
            except Exception as e:
                logger.warning(f"⚠️  Error closing page: {e}")

        if context is not None:
            try:
                context.close()
                logger.info("✓ Context closed")
            except Exception as e:
                logger.warning(f"⚠️  Error closing context: {e}")

    yield

@pytest.fixture(scope="function")
def authenticated_page(page):
    """
    Provides a page with user already authenticated via stored session.
    
    Apply stealth mode to hide Playwright from bot detection.
    """
    # Apply stealth mode
    stealth(page)
    logger.info("✓ Stealth mode applied to authenticated_page")
    
    page.set_default_timeout(Config.DEFAULT_TIMEOUT)
    page.goto(Config.BASE_URL)
    
    # Small wait to ensure page is ready
    page.wait_for_timeout(2000)
    logger.info(f"✓ Navigated to: {Config.BASE_URL}")
    
    return page

# ============================================================================

@pytest.fixture
def api_client(playwright):
    """
    Provides APIClient with proper resource cleanup.

    The request context must be disposed after test completion.
    Using try-finally pattern to ensure cleanup even if test fails.
    """
    request_context = playwright.request.new_context()

    try:
        client = APIClient(request_context)
        yield client
    finally:
        # Mandatory: dispose the request context after the test
        try:
            request_context.dispose()
        except Exception as e:
            print(f"⚠️  Error disposing request context: {e}")

@pytest.fixture
def utils():
    return Helpers()

@pytest.fixture
def home_page_obj(page: Page) -> HomePage:
    """
    Provides HomePage instance with automatic navigation.

    Usage:
        def test_homepage(home_page_obj: HomePage):
            home_page_obj.search_for_product("hammer")
            assert home_page_obj.get_product_count() > 0
    """
    home_page_obj = HomePage(page)
    page.goto(Config.BASE_URL)
    page.wait_for_timeout(5000)

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
        def test_modal(home_page_obj: HomePage, wait_for_animation):
            home_page_obj.open_modal_button.click()
            wait_for_animation(500)  # Wait 500ms
            expect(home_page_obj.modal).to_be_visible()
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
        def test_search_products(home_page_obj: HomePage, search_term: str):
            # This test runs 3 times (hammer, screwdriver, pliers)
            home_page_obj.search_for_product(search_term)
            assert home_page_obj.get_product_count() > 0
    """
    return request.param
