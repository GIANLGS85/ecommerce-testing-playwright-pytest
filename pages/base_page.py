from playwright.sync_api import Page, Locator, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from typing import Optional
import logging
import re
import time

logger = logging.getLogger(__name__)


async def click_element(locator: Locator):
    try:
        await locator.wait_for(state="visible")
        await locator.highlight()
        await locator.click()
    except Exception as e:
        logger.error(f"Click failed on {locator}: {e}")
        raise


class BasePage:
    """
    Base class for all page objects.
    
    Provides common functionality that all pages need.
    Each page object should inherit from this.

    """
    
    def __init__(self, page: Page):
        """
        Initialize BasePage.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.timeout = 30000  # Default timeout in milliseconds
    
    # ========================================
    # NAVIGATION METHODS
    # ========================================

    def navigate_to(self, url: str):
        """
        Navigate to a specific URL.
        
        Args:
            url: Full URL to navigate to
        """
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)
        self.wait_for_page_load()
    
    def refresh(self):
        """Refresh/reload the current page."""
        logger.info("Refreshing page")
        self.page.reload()
        self.wait_for_page_load()
    
    def go_back(self):
        """Navigate back in browser history."""
        logger.info("Going back")
        self.page.go_back()
        self.wait_for_page_load()
    
    def get_current_url(self) -> str:
        """
        Get current page URL.
        
        Returns:
            Current URL as string
        """
        return self.page.url
    
    def get_title(self) -> str:
        """
        Get page title.
        
        Returns:
            Page title as string
        """
        return self.page.title()
    
    # ========================================
    # WAITING METHODS
    # ========================================
    
    def wait_for_page_load(self):
        """Wait for page to fully load (DOM + network idle)."""
        self.page.wait_for_load_state("domcontentloaded")
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except:
            pass  # Network idle is nice-to-have, not required
    
    def wait_for_element(self, locator: Locator, timeout: Optional[int] = None):
        """
        Wait for element to be visible.
        
        Args:
            locator: Playwright Locator object
            timeout: Max wait time in milliseconds (optional)
        """
        timeout = timeout or self.timeout
        logger.info(f"Waiting for element to be visible")
        expect(locator).to_be_visible(timeout=timeout)
    
    def wait_for_element_hidden(self, locator: Locator, timeout: Optional[int] = None):
        """
        Wait for element to be hidden.
        
        Args:
            locator: Playwright Locator object
            timeout: Max wait time in milliseconds (optional)
        """
        timeout = timeout or self.timeout
        logger.info(f"Waiting for element to be hidden")
        expect(locator).to_be_hidden(timeout=timeout)
    
    def wait_for_url_contains(self, text: str, timeout: Optional[int] = None):
        """
        Wait for URL to contain specific text.
        
        Args:
            text: Text that should be in URL
            timeout: Max wait time in milliseconds (optional)
        """
        timeout = timeout or self.timeout
        logger.info(f"Waiting for URL to contain: {text}")
        self.page.wait_for_url(f"**/*{text}*", timeout=timeout)
    
    def wait(self, milliseconds: int):
        """
        Hard wait for specified time.
        
        WARNING: Use sparingly! Prefer wait_for_element() instead.
        
        Args:
            milliseconds: Time to wait in milliseconds
        """
        logger.warning(f"Hard wait for {milliseconds}ms")
        self.page.wait_for_timeout(milliseconds)

        
        
    def wait_until_locator_count_stable(self, locator: Locator, timeout=5000, poll_interval=300):
        """
        ChagGPT (use this only if the CLAUDE method (wait_for_content_loaded) does not work)
        """
        
        end_time = time.time() + timeout / 1000
        last_count = -1

        while time.time() < end_time:
            current_count = locator.count()

            if current_count == last_count and current_count > 0:
                return

            last_count = current_count
            time.sleep(poll_interval / 1000)

        raise TimeoutError("Locator count did not stabilize")

    
    def wait_for_content_loaded(self, timeout: int = 5000):
        """THE universal wait method.
        CLAUDE
        """
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except:
            pass
        self._wait_for_dom_stable(timeout=2000)
        time.sleep(0.1)
    
    def _wait_for_dom_stable(self, timeout: int = 2000):
        """Internal helper.
        CLAUDE
        """
        end_time = time.time() + timeout / 1000
        last_state = None
        stable_count = 0
        
        while time.time() < end_time:
            try:
                current_state = self.page.evaluate("document.body.innerHTML.length")
            except:
                current_state = 0
            
            if current_state == last_state and current_state > 0:
                stable_count += 1
                if stable_count >= 2:
                    return
            else:
                stable_count = 0
            
            last_state = current_state
            time.sleep(0.3)
        return
    
        
    
    def wait_for_dom_update(self, container: Locator, *, settle_ms: int = 250, timeout_ms: int = 5000,):
        """
        Copilot's method (with ChatGPT's review and improvements)
        
        Wait until the given container finishes updating its DOM.
        Safe for search, filter, sort, pagination.

        - settle_ms: how long DOM must stay unchanged
        - timeout_ms: max wait before failing
        
        page.evaluate() means:
        Run this JavaScript inside the actual webpage.
        container.element_handle() gives the JS function a reference to your product list container.
        """
        
        print("COUNT:", container.count())
        
        script = r"""
                    async (container, settleMs, timeoutMs) => {
                        return await new Promise((resolve, reject) => {
                            let settleTimer = null;
                            let timeoutTimer = null;

                            const done = () => {
                                observer.disconnect();
                                clearTimeout(settleTimer);
                                clearTimeout(timeoutTimer);
                                resolve();
                            };

                            const observer = new MutationObserver(() => {
                                clearTimeout(settleTimer);
                                settleTimer = setTimeout(done, settleMs);
                            });

                            observer.observe(container, {
                                childList: true,
                                subtree: true,
                                attributes: true,
                                characterData: true,
                            });

                            timeoutTimer = setTimeout(() => {
                                observer.disconnect();
                                reject("DOM did not stabilize in time");
                            }, timeoutMs);
                        });
                    }
                """

        handle = container.element_handle() 
        if handle is None: raise RuntimeError("Container element not found or not unique") 
        
        try: 
            self.page.evaluate(script, handle) 
        except Exception as e: 
            raise PlaywrightTimeoutError(str(e)) 
        


    # ========================================
    # ASSERTION HELPERS
    # ========================================
    
    def assert_url_contains(self, text: str):
        """
        Assert URL contains specific text.
        
        Args:
            text: Text that should be in URL
        """
        logger.info(f"Asserting URL contains: {text}")
        expect(self.page).to_have_url(re.compile(f".*{re.escape(text)}.*"))
    
    def assert_url_is(self, url: str):
        """
        Assert exact URL match.
        
        Args:
            url: Expected full URL
        """
        logger.info(f"Asserting URL is: {url}")
        expect(self.page).to_have_url(url)
    
    def assert_url_matches(self, pattern: str):
        """
        Assert URL matches regex pattern.
        
        Args:
            pattern: Regex pattern (e.g., ".*/auth/login")
        """
        logger.info(f"Asserting URL matches pattern: {pattern}")
        expect(self.page).to_have_url(re.compile(pattern))
    
    def assert_title_is(self, title: str):
        """
        Assert exact page title.
        
        Args:
            title: Expected page title
        """
        logger.info(f"Asserting title is: {title}")
        expect(self.page).to_have_title(title)
    
    def assert_title_contains(self, text: str):
        """
        Assert page title contains text.
        
        Args:
            text: Text that should be in title
        """
        logger.info(f"Asserting title contains: {text}")
        expect(self.page).to_have_title(re.compile(f".*{re.escape(text)}.*"))
    
    @staticmethod
    def assert_element_visible(locator: Locator):
        """
        Assert element is visible.
        
        Args:
            locator: Playwright Locator object
        """
        logger.info(f"Asserting element {locator.all_inner_texts()} is visible")
        expect(locator).to_be_visible()
    
    @staticmethod
    def assert_element_hidden(locator: Locator):
        """
        Assert element is hidden.
        
        Args:
            locator: Playwright Locator object
        """
        logger.info("Asserting element is hidden")
        expect(locator).to_be_hidden()
    
    def assert_text_visible(self, text: str):
        """
        Assert text is visible somewhere on the page.
        
        Args:
            text: Text to search for
        """
        logger.info(f"Asserting text is visible: {text}")
        expect(self.page.get_by_text(text)).to_be_visible()
        
    @staticmethod
    def assert_search_term(locator: Locator, expected: str) -> None:
        """ Assert that the <span data-test="search-term"> element contains the expected search term. 
        Parameters: locator (Locator): Playwright locator pointing to the search-term element. expected (str): 
        The expected text value (e.g., "hammer"). """ 
        expect(locator).to_have_text(expected, ignore_case=True)
    
    # ========================================
    # ELEMENT INTERACTION HELPERS
    # ========================================
    
    def get_text(self, locator: Locator) -> str:
        """
        Get text content of element.
        
        Args:
            locator: Playwright Locator object
            
        Returns:
            Element text content
        """
        return locator.inner_text()
    
    def get_attribute(self, locator: Locator, attribute: str) -> Optional[str]:
        """
        Get element attribute value.
        
        Args:
            locator: Playwright Locator object
            attribute: Attribute name (e.g., "href", "class")
            
        Returns:
            Attribute value or None
        """
        return locator.get_attribute(attribute)
    
    def is_visible(self, locator: Locator) -> bool:
        """
        Check if element is visible.
        
        Args:
            locator: Playwright Locator object
            
        Returns:
            True if visible, False otherwise
        """
        return locator.is_visible()
    
    def is_enabled(self, locator: Locator) -> bool:
        """
        Check if element is enabled.
        
        Args:
            locator: Playwright Locator object
            
        Returns:
            True if enabled, False otherwise
        """
        return locator.is_enabled()
    
    def get_element_count(self, locator: Locator) -> int:
        """
        Get count of elements matching locator.
        
        Args:
            locator: Playwright Locator object
            
        Returns:
            Number of matching elements
        """
        return locator.count()
    
    def get_collection_count_safe(self, locator: Locator, minimum=1) -> int:
        """
        Get product count safely (waits for products first).
        
        Returns:
            Number of products
        """
        locator.first.wait_for(state="visible") 
        count = locator.count() 
        if count < minimum: 
            raise AssertionError(f"Expected at least {minimum} elements, got {count}")
        else:
            logger.info(f"There are {count} products found")
            
        return count
    
    # ========================================
    # SCROLLING METHODS
    # ========================================
    
    def scroll_to_element(self, locator: Locator):
        """
        Scroll element into view.
        
        Args:
            locator: Playwright Locator object
        """
        logger.info("Scrolling to element")
        locator.scroll_into_view_if_needed()
    
    def scroll_to_top(self):
        """Scroll to top of page."""
        logger.info("Scrolling to top")
        self.page.evaluate("window.scrollTo(0, 0)")
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page."""
        logger.info("Scrolling to bottom")
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    
    # ========================================
    # DEBUGGING HELPERS
    # ========================================
    
    def pause(self):
        """
        Pause test execution and open Playwright Inspector.
        
        Use for debugging. Remove before committing.
        """
        logger.info("⏸️  Pausing for debugging (Playwright Inspector)")
        self.page.pause()
    
    def take_screenshot(self, name: str):
        """
        Take a screenshot.
        
        Args:
            name: Filename (without extension)
        """
        filename = f"screenshots/{name}.png"
        logger.info(f"📸 Taking screenshot: {filename}")
        self.page.screenshot(path=filename)
    
    def take_full_screenshot(self, name: str):
        """
        Take a full page screenshot.
        
        Args:
            name: Filename (without extension)
        """
        filename = f"screenshots/{name}.png"
        logger.info(f"📸 Taking full page screenshot: {filename}")
        self.page.screenshot(path=filename, full_page=True)
    
    # ========================================
    # ADVANCED UTILITIES (Use Rarely)
    # ========================================
    
    def execute_javascript(self, script: str):
        """
        Execute JavaScript in browser context.
        
        Args:
            script: JavaScript code to execute
            
        Returns:
            Result of script execution
        """
        logger.info(f"Executing JavaScript: {script[:50]}...")
        return self.page.evaluate(script)
    
    def get_local_storage_item(self, key: str) -> Optional[str]:
        """
        Get item from localStorage.
        
        Args:
            key: localStorage key
            
        Returns:
            Value from localStorage or None
        """
        return self.page.evaluate(f"localStorage.getItem('{key}')")
    
    def set_local_storage_item(self, key: str, value: str):
        """
        Set item in localStorage.
        
        Args:
            key: localStorage key
            value: Value to store
        """
        self.page.evaluate(f"localStorage.setItem('{key}', '{value}')")
    
    def clear_local_storage(self):
        """Clear all localStorage."""
        logger.info("Clearing localStorage")
        self.page.evaluate("localStorage.clear()")
    
    def get_cookies(self):
        """
        Get all cookies.
        
        Returns:
            List of cookie dictionaries
        """
        return self.page.context.cookies()
    
    def clear_cookies(self):
        """Clear all cookies."""
        logger.info("Clearing cookies")
        self.page.context.clear_cookies()


# ========================================
# USAGE EXAMPLE
# ========================================

"""
Example HomePage using BasePage:

from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Define locators
        self.search_input = page.locator('[data-test="search-query"]')
        self.search_button = page.locator('[data-test="search-submit"]')
        self.products = page.locator(".product-card")
    
    def search_for_product(self, product_name: str):
        self.search_input.fill(product_name)
        self.search_button.click()
        self.wait_for_page_load()
    
    def get_product_count(self) -> int:
        return self.get_element_count(self.products)


# In tests:
def test_search(home_page_obj: HomePage):
    home_page_obj.search_for_product("hammer")
    home_page_obj.assert_url_contains("q=hammer")
    assert home_page_obj.get_product_count() > 0
"""