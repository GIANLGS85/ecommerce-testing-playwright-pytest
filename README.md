# E-commerce E2E Automation Testing Framework (Playwright)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Playwright](https://img.shields.io/badge/Playwright-1.58.0%2B-orange)
![Pytest](https://img.shields.io/badge/Pytest-9.0-yellow)
![Status](https://img.shields.io/badge/Status-Maintained-brightgreen)

## Project Introduction
This project is a modern E2E automation testing framework designed specifically for high-concurrency e-commerce transactions, designed to test the training wemsite https://practicesoftwaretesting.com/ of which the documentation can be found here:  https://github.com/testsmith-io/practice-software-testing

Developed with Playwright and Python, the framework manages dynamic web interfaces and validates API interactions.
It adopts the Page Object Model (POM) architecture and supports CSV‑driven test data, ensuring consistent and reliable validation from front‑end user flows to back‑end accounting processes.

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
| Programming Language | Python 3.12+ | Core development language |
| Automation Engine | Playwright | Next-gen browser automation (Supports Chromium, Firefox, WebKit) |
| Test Runner | Pytest | Test case management and Fixture implementation |
| Data Processing | Pandas | Handles large-scale Excel/CSV test data |
| Test Reporting | Allure Report | Generates visual reports with screenshots and charts |
| Env Management | Python-dotenv | Manages sensitive information (e.g., DB credentials) for security |

---

## Project Structure
The project uses a standard layered architecture to ensure high readability and scalability:
```text
ecommerce-playwright-pytest/
│ 
├── pages/
│   ├── components/
│   │   ├── header.py
│   │   ├── filters.py
│   │   ├── __init__.py
│   │   ├── search_bar.py
│   │   ├── product_grid.py
│   │   └── project_locators/
│   │       ├── __init__.py
│   │       ├── pages_locators.py
│   │       └── components_locators.py
│   ├── __init__.py
│   ├── base_page.py
│   ├── cart_page.py
│   ├── home_page.py
│   ├── login_page.py
│   └── product_details_page.py
├── tests/
│   ├── UI/
│   │   ├── __init__.py
│   │   ├── test_checkout.py
│   │   ├── test_Discovery.py
│   │   ├── test_home_search.py
│   │   ├── test_home_filters.py
│   │   └── test_home_navigation.py
│   ├── API/
│   │   ├── __init__.py
│   │   ├── test_brands.py
│   │   └── test_products.py
│   ├── SmokeTests/
│   │   ├── __init__.py
│   │   ├── test_home_smoke.py
│   │   └── test_home_open_MINI.py
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_login.py
│   └── UI-UnstableTests/
├── utils/
│   ├── helpers.py
│   ├── __init__.py
│   ├── api_client.py
│   └── data_loader.py
├── config/
│   ├── config.py
│   └── __init__.py
├── LICENSE
├── README.md
├── test_data/
│   ├── test_orders.csv
│   └── checkout_data.csv
├── playwright/
│   └── .auth/    # used to store session cookies
├── conftest.py
└── requirements.txt
```

