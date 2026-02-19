# E-commerce E2E Automation Testing Framework (Playwright)

![Python](https://img.shields.io/badge/Python-3.14%2B-blue)
![Playwright](https://img.shields.io/badge/Playwright-1.58.0%2B-orange)
![Pytest](https://img.shields.io/badge/Pytest-9.0-yellow)
![Status](https://img.shields.io/badge/Status-Maintained-brightgreen)

## Project Introduction
This project is a modern E2E automation testing framework designed specifically for high-concurrency e-commerce transactions.

Developed using Playwright and Python, it effectively resolves the instability issues found in traditional tools (like Selenium) when handling dynamic web pages. The framework strictly follows the Page Object Model (POM) design pattern and integrates MySQL database verification and Excel data-driven testing. This ensures consistency and precision from front-end UI operations to back-end accounting records.

---

## Core Technical Features
* Extreme Stability (Auto-wait Mechanism):
    Leverages Playwright’s built-in auto-wait functionality to eliminate flaky tests caused by network latency or incomplete page rendering. No manual sleep commands are required.
* Modular Architecture (POM):
    Implements the Page Object Model to completely decouple "element locators" from "business logic." When the UI is updated, only a single page object needs maintenance, significantly reducing long-term costs.
* Network Interception & Mocking:
    Utilizes Playwright to intercept network requests, allowing for the simulation of third-party payment (e.g., LINE Pay) timeouts or failures to verify the system's error-handling mechanisms.
* Data-Driven Testing:
    Integrates Pandas to read Excel/CSV test data. Through parameterized execution, a single script can cover multiple boundary cases (e.g., different currencies or inventory thresholds).
* Dual UI & DB Verification:
    Beyond verifying visual success, the framework automatically connects to a MySQL database after transactions to check if order statuses and inventory deductions are accurate, preventing accounting loopholes.
* Visual Debugging:
    Automatically preserves full execution traces upon test failure (including screenshots, videos, and network logs) to help developers replay and pinpoint issues quickly.

---

## 🛠 Tech Stack
| Component | Tool / Package | Description |
| :--- | :--- | :--- |
| Programming Language | Python 3.9+ | Core development language |
| Automation Engine | Playwright | Next-gen browser automation (Supports Chromium, Firefox, WebKit) |
| Test Runner | Pytest | Test case management and Fixture implementation |
| Data Processing | Pandas | Handles large-scale Excel/CSV test data |
| DB Verification | PyMySQL | Database connectivity for SQL validation |
| Test Reporting | Allure Report | Generates visual reports with screenshots and charts |
| Env Management | Python-dotenv | Manages sensitive information (e.g., DB credentials) for security |

---

## Project Structure
The project uses a standard layered architecture to ensure high readability and scalability:
```text
├── config/              # Global configurations (Base URL, browser params, timeout settings)
├── pages/               # Page Object Model (POM) - Encapsulates locators and methods
│   └──components
|	├──project_locators
|	|  ├──components_locators.py 
|	|  └──pages_locators.py 
|	├─filters.py
|	├─header.py
|	├─pagination.py
|	├─product_grid.py
|	└──search_bar.py
|	
├── base_page.py     # Base methods (Encapsulated waiting and exception handling)
|    ├── login_page.py    # Login page logic
|    ├── home_page.py ....# Home page logic
|    └── checkout_page.py # Checkout and transaction flow logic
|
├── tests/               # Test Script Layer - Business logic and assertions
│   ├── conftest.py      # Pytest Fixtures (Browser environment setup, shared login states)
│   ├── test_login.py    # Login functionality tests
│   └── test_checkout.py # Checkout process tests
├── test_data/           # Test Data Storage (Excel/CSV files)
├─utils/
│   ├── __init__.py
│   ├── helpers.py          # Network/Business logic
│   └── api_client.py       # General tools/Data generation
├── requirements.txt     # Project dependencies list
├── pytest.ini           # Pytest configuration file
└── README.md            # Project documentation
```

## Examples
here below usage example of few tests against the HomePage:
```text


from playwright.sync_api import Page, expect
from pages.home_page import HomePage
import pytest


@pytest.fixture
def home_page_obj(page: Page) -> HomePage:
    page.goto("https://your-site.com")
    return HomePage(page)


def test_search_for_product(home_page_obj: HomePage):
    # Multi-step action - use method
    home_page_obj.search_for_product("hammer")
    
    # Assertion - use BasePage method
    home_page_obj.assert_url_contains("q=hammer")
    
    # Getter - use method
    assert home_page_obj.get_product_count() > 0


def test_navigate_to_signin(home_page_obj: HomePage):
    # Simple click - use locator directly
    home_page_obj.signin_link.click()
    
    # Assertion - use BasePage method
    home_page_obj.assert_url_contains("/auth/login")


def test_filter_and_sort(home_page_obj: HomePage):
    # Complex actions - use methods
    home_page_obj.filter_by_category("Hand Tools")
    home_page_obj.filter_by_price_range(min_price=10, max_price=50)
    home_page_obj.sort_by_label("Price (Low - High)")
    
    # Verification - use method
    assert home_page_obj.is_products_sorted_by_price_ascending()


def test_add_to_cart(home_page_obj: HomePage):
    # Simple clicks - use locators directly
    home_page_obj.first_product.click()
    
    # On product detail page
    home_page_obj.page.locator('[data-test="add-to-cart"]').click()
    
    # Go back and verify cart
    home_page_obj.go_back()
    assert home_page_obj.get_cart_count() == 1

```

