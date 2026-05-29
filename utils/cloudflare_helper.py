"""
Cloudflare Bypass Helper for Playwright

This module provides utilities to bypass Cloudflare protection using cloudscraper,
then injects the clearance cookies into Playwright for authenticated sessions.

Strategy:
    1. Use cloudscraper to resolve Cloudflare JS Challenge
    2. Extract clearance cookies
    3. Inject into Playwright context
    4. Apply stealth mode to hide Playwright
"""

import cloudscraper
import logging
from typing import Dict
from playwright.sync_api import Page, BrowserContext

logger = logging.getLogger(__name__)


class CloudflareHelper:
    """
    Helper class for bypassing Cloudflare protection with Playwright.

    Uses cloudscraper to pre-solve Cloudflare challenge, then injects
    the clearance cookies into Playwright for seamless authentication.
    """

    # Cloudflare clearance cookie names to look for
    CLOUDFLARE_COOKIE_NAMES = ["cf_clearance", "cfrequestid"]

    @staticmethod
    def get_cloudflare_cookies(url: str, timeout: int = 30) -> Dict[str, str]:
        """
        Bypass Cloudflare JS Challenge and extract clearance cookies.

        This function uses cloudscraper to automatically solve Cloudflare's
        JavaScript challenge and extracts the resulting cookies that confirm
        the browser is legitimate.

        Args:
            url (str):
                The URL to bypass Cloudflare for.
                Example: "https://practicesoftwaretesting.com/"

            timeout (int, optional):
                Request timeout in seconds. Defaults to 30.

        Returns:
            Dict[str, str]:
                Dictionary of cookies from the successful Cloudflare bypass.
                Key is cookie name, value is cookie value.

        Raises:
            Exception: If cloudscraper fails to bypass Cloudflare.

        Example:
            >>> cookies = CloudflareHelper.get_cloudflare_cookies(
            ...     "https://practicesoftwaretesting.com/"
            ... )
            >>> print(cookies)
            {'cf_clearance': 'abc123...', 'cfrequestid': 'xyz789...'}
        """
        logger.info(f"🔵 Attempting Cloudflare bypass for: {url}")

        try:
            # Create scraper that automatically handles Cloudflare
            scraper = cloudscraper.create_scraper()

            # Make request - cloudscraper solves challenge automatically
            logger.info("→ Making request with cloudscraper...")
            response = scraper.get(url, timeout=timeout)

            # Extract all cookies
            cookies = scraper.cookies.get_dict()

            # Filter for Cloudflare-specific cookies
            cf_cookies = {
                k: v for k, v in cookies.items()
                if any(cf_name in k.lower() for cf_name in CloudflareHelper.CLOUDFLARE_COOKIE_NAMES)
            }

            if cf_cookies:
                logger.info(f"✅ Cloudflare bypass SUCCESS!")
                logger.info(f"   Clearance cookies found: {list(cf_cookies.keys())}")
                logger.info(f"   All cookies extracted: {len(cookies)}")
            else:
                logger.warning(f"⚠️  No Cloudflare clearance cookies found")
                logger.info(f"   Available cookies: {list(cookies.keys())}")
                # Return all cookies anyway - might still work
                cf_cookies = cookies

            return cf_cookies

        except Exception as e:
            logger.error(f"❌ Cloudflare bypass FAILED: {str(e)}")
            logger.error(f"   URL: {url}")
            raise

    @staticmethod
    def inject_cookies_to_context(
        context: BrowserContext,
        cookies: Dict[str, str],
        domain: str,
    ) -> None:
        """
        Inject cookies into Playwright browser context.

        Converts cookie dictionary into Playwright cookie format and adds
        them to the context. These cookies will be sent with all requests
        in this context.

        Args:
            context (BrowserContext):
                Playwright browser context to inject cookies into.

            cookies (Dict[str, str]):
                Dictionary of cookies (name -> value).
                Typically from get_cloudflare_cookies().

            domain (str):
                Domain for the cookies.
                Example: "practicesoftwaretesting.com"

        Returns:
            None

        Side Effects:
            Adds cookies to the context. Subsequent page navigations
            will include these cookies.

        Example:
            >>> cookies = CloudflareHelper.get_cloudflare_cookies(url)
            >>> CloudflareHelper.inject_cookies_to_context(
            ...     context,
            ...     cookies,
            ...     "practicesoftwaretesting.com"
            ... )
        """
        logger.info(f"💉 Injecting cookies into context for domain: {domain}")

        # Convert dict format to Playwright cookie format
        playwright_cookies = [
            {
                "name": name,
                "value": value,
                "domain": domain,
                "path": "/",
                "expires": -1,  # Session cookie
                "httpOnly": False,
                "secure": True,
                "sameSite": "None"
            }
            for name, value in cookies.items()
        ]

        try:
            # Add cookies to context
            context.add_cookies(playwright_cookies)
            logger.info(f"✓ Injected {len(playwright_cookies)} cookies")
            logger.debug(f"  Cookies: {[c['name'] for c in playwright_cookies]}")

        except Exception as e:
            logger.error(f"❌ Failed to inject cookies: {e}")
            raise

    @staticmethod
    def inject_cookies_to_page(
        page: Page,
        cookies: Dict[str, str],
        domain: str,
    ) -> None:
        """
        Inject cookies into Playwright page (via context).

        Convenience method that injects cookies into the page's context.

        Args:
            page (Page): Playwright page object.
            cookies (Dict[str, str]): Dictionary of cookies.
            domain (str): Cookie domain.

        Returns:
            None

        Example:
            >>> cookies = CloudflareHelper.get_cloudflare_cookies(url)
            >>> CloudflareHelper.inject_cookies_to_page(
            ...     page,
            ...     cookies,
            ...     "practicesoftwaretesting.com"
            ... )
        """
        CloudflareHelper.inject_cookies_to_context(
            page.context,
            cookies,
            domain
        )

    @staticmethod
    def verify_cloudflare_bypass(page: Page, base_url: str) -> bool:
        """
        Verify that Cloudflare bypass was successful.

        Attempts to navigate to URL and checks if page loads without
        Cloudflare challenge page.

        Args:
            page (Page): Playwright page object.
            base_url (str): URL to verify against.

        Returns:
            bool: True if page loaded without challenge, False otherwise.

        Example:
            >>> success = CloudflareHelper.verify_cloudflare_bypass(
            ...     page,
            ...     "https://practicesoftwaretesting.com/"
            ... )
            >>> if success:
            ...     print("✅ Cloudflare bypass verified!")
        """
        logger.info(f"🔍 Verifying Cloudflare bypass for: {base_url}")

        try:
            page.goto(base_url, wait_until="domcontentloaded")

            # Check if we got challenge page (contains 'challenge' or 'Cloudflare')
            page_title = page.title()
            page_url = page.url

            if "challenge" in page_title.lower() or "challenge" in page_url.lower():
                logger.warning(f"⚠️  Cloudflare challenge page detected!")
                logger.warning(f"   Title: {page_title}")
                logger.warning(f"   URL: {page_url}")
                return False

            logger.info(f"✅ Cloudflare bypass verified!")
            logger.info(f"   Page loaded successfully")
            logger.info(f"   Title: {page_title}")
            return True

        except Exception as e:
            logger.error(f"❌ Verification failed: {e}")
            return False

    @staticmethod
    def save_cookies_to_file(cookies: Dict[str, str], filepath: str) -> None:
        """
        Save cookies to JSON file for debugging/inspection.

        Args:
            cookies (Dict[str, str]): Cookies to save.
            filepath (str): Path to save JSON file.
        """
        import json
        try:
            with open(filepath, 'w') as f:
                json.dump(cookies, f, indent=2)
            logger.info(f"✓ Cookies saved to: {filepath}")
        except Exception as e:
            logger.warning(f"⚠️  Failed to save cookies: {e}")

    @staticmethod
    def load_cookies_from_file(filepath: str) -> Dict[str, str]:
        """
        Load cookies from JSON file.

        Args:
            filepath (str): Path to JSON cookie file.

        Returns:
            Dict[str, str]: Loaded cookies.
        """
        import json
        try:
            with open(filepath, 'r') as f:
                cookies = json.load(f)
            logger.info(f"✓ Cookies loaded from: {filepath}")
            return cookies
        except Exception as e:
            logger.error(f"❌ Failed to load cookies: {e}")
            raise

