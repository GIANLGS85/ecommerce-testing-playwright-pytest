import random
import string
import re
from datetime import datetime
from typing import Dict, Optional
from playwright.sync_api import Page

class Helpers:
    """General utility toolbox for data generation and UI interactions."""

    @staticmethod
    def generate_test_user_payload() -> Dict[str, str]:
        """Generates a raw dictionary for API or Form injection."""
        uid = ''.join(random.choices(string.digits, k=5))
        return {
            "first_name": "Test",
            "last_name": f"User_{uid}",
            "email": f"test_{uid}@example.com",
            "password": "SecurePass123!"
        }

    @staticmethod
    def extract_price(text: str) -> Optional[float]:
        """Cleans currency strings into floats (e.g., '$1,200.50' -> 1200.5)."""
        clean_text = re.sub(r'[^\d.]', '', text.replace(',', ''))
        return float(clean_text) if clean_text else None

    @staticmethod
    def take_screenshot(page: Page, name: str):
        """Standardized screenshot utility."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/{name}_{timestamp}.png")