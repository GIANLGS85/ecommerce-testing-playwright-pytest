"""
============================================================================
GLOBAL CONFTEST.PY - Master Template
============================================================================
Copy this file to every new Playwright Python project

Features:
✅ Timestamped results folder (complete test history)
✅ Beautiful test execution banners with emojis
✅ Real-time PASS/FAIL/SKIP reporting
✅ Automatic screenshots on test failure
✅ Automatic cleanup of invalid video files
✅ Results always saved to project root
✅ Works from any directory

Results Structure:
results_Playwright/
├── 2025-11-24_09-56-53/    ← First test run
│   ├── test-report.html
│   ├── test-logs.log
│   ├── screenshots/
│   └── videos/
├── 2025-11-24_10-15-30/    ← Second test run
│   ├── test-report.html
│   ├── test-logs.log
│   ├── screenshots/
│   └── videos/
└── 2025-11-24_14-22-45/    ← Third test run

============================================================================
"""

import pytest
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# TIMESTAMPED RESULTS DIRECTORY
# ============================================================================

def pytest_configure(config):
    """
    Setup before any tests run (called ONCE per session)
    
    Creates timestamped results directory and configures paths.
    Results are ALWAYS saved to project root, regardless of where
    you run pytest from.
    
    What it does:
    1. Creates timestamped folder (YYYY-MM-DD_HH-MM-SS)
    2. Sets HTML report path
    3. Sets video output path
    4. Sets log file path
    5. Stores config for later use
    """
    
    # Generate timestamp for this test run
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Find project root (where pytest.ini is located)
    project_root = Path(config.rootpath)  # Playwright finds this automatically
    print("\nPytest rootpath:", config.rootpath)
    logger.info(f"Detected pytest rootpath: {project_root}")
    
    # Create timestamped folder at project root
    results_base = project_root / "results_Playwright"
    results_dir = results_base / timestamp
    results_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"*** SESSION START: Creating {results_dir} ***")
    
    # Set HTML report path (pytest-html)
    config.option.htmlpath = str(results_dir / "test-report.html")
    
    # Set Playwright video output path
    config.option.output = str(results_dir / "videos")
    
    # Configure file logging
    log_file_path = str(results_dir / "test-logs.log")
    config.option.log_file = log_file_path
    config.option.log_file_level = "INFO"
    config.option.log_file_format = "%(asctime)s [%(levelname)8s] %(message)s"
    config.option.log_file_date_format = "%Y-%m-%d %H:%M:%S"
    
    # Force enable file logging (ensures logs are written)
    if hasattr(config, '_inicache'):
        config._inicache['log_file'] = log_file_path
        config._inicache['log_file_level'] = "INFO"

    
    # Store results_dir for use in fixtures
    config.results_dir = results_dir
    
    # Print configuration info
    print(f"\n{'='*70}")
    print(f"📁 PROJECT CONFIGURATION")
    print(f"{'='*70}")
    print(f"Project Root: {project_root}")
    print(f"Results Dir:  {results_dir}")
    print(f"HTML Report:  {results_dir / 'test-report.html'}")
    print(f"Log File:     {log_file_path}")
    print(f"{'='*70}\n")


# ============================================================================
# PYTEST HOOKS - TEST EXECUTION
# ============================================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    """
    Display test start banner
    
    Runs BEFORE each test starts.
    Shows which test is about to run with timestamp.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n{'='*70}")
    print(f"🧪 STARTING: {item.nodeid}")
    print(f"⏰ Time: {timestamp}")
    print(f"{'='*70}\n")
    
    yield # Let the test run


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Display test result and track failures
    
    Runs AFTER each test completes.
    - Shows PASS/FAIL/SKIP status with timestamp
    - Tracks failures for screenshot capture
    """
    outcome = yield
    report = outcome.get_result()
    
    # Track failure status for screenshots
    if report.when == "call" and report.failed:
        pytest.current_test_failed = True
        pytest.current_test_item = item
    else:
        pytest.current_test_failed = False
    
    # Display result banner (only for actual test execution)
    if report.when == "call":
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if report.passed:
            print(f"\n{'='*70}")
            print(f"✅ PASSED: {item.name}")
            print(f"⏰ Time: {timestamp}")
            print(f"{'='*70}\n")
            
        elif report.failed:
            print(f"\n{'='*70}")
            print(f"❌ FAILED: {item.name}")
            print(f"⏰ Time: {timestamp}")
            print(f"{'='*70}\n")
            
        elif report.skipped:
            print(f"\n{'='*70}")
            print(f"⏭️  SKIPPED: {item.name}")
            print(f"⏰ Time: {timestamp}")
            print(f"{'='*70}\n")


def pytest_sessionfinish(session, exitstatus):
    """
    Cleanup and summary after ALL tests complete
    
    Runs ONCE after entire test session finishes.
    - Removes invalid .png files from videos folder
    - Displays final summary
    """
    print(f"\n{'='*70}")
    print(f"🎉 TEST SESSION COMPLETED")
    print(f"{'='*70}")
    
    # Cleanup invalid video metadata files
    if hasattr(session.config, 'results_dir'):
        results_dir = session.config.results_dir
        videos_dir = results_dir / "videos"
        
        if videos_dir.exists():
            png_count = 0
            for png_file in videos_dir.rglob("*.png"):
                try:
                    png_file.unlink()
                    png_count += 1
                except Exception:
                    pass  # Silently ignore errors
            
            if png_count > 0:
                print(f"🧹 Cleaned up {png_count} invalid video file(s)")
    
    # Display exit status
    if exitstatus == 0:
        print(f"✅ ALL TESTS PASSED!")
    elif exitstatus == 1:
        print(f"❌ SOME TESTS FAILED")
    elif exitstatus == 2:
        print(f"⚠️  TEST EXECUTION INTERRUPTED")
    elif exitstatus == 3:
        print(f"⚠️  INTERNAL ERROR")
    elif exitstatus == 4:
        print(f"⚠️  PYTEST USAGE ERROR")
    elif exitstatus == 5:
        print(f"⚠️  NO TESTS COLLECTED")
    
    print(f"{'='*70}\n")


# ============================================================================
# FIXTURES - AUTOMATIC SETUP
# ============================================================================

@pytest.fixture(scope="function", autouse=True)
def page_setup(page, request):
    """
    Automatic setup for EVERY test
    
    autouse=True means this runs automatically for all tests.
    
    BEFORE test:
    - Sets default timeout to 10 seconds
    
    AFTER test:
    - Takes screenshot if test failed
    - Saves to timestamped results folder
    
    Args:
        page: Playwright page fixture (from pytest-playwright)
        request: Pytest request object (for accessing config)
    """
    page.set_default_timeout(10000)
    
    yield page # Test runs here
    
    # TEARDOWN - After test completes
    # Take screenshot if test failed
    if hasattr(pytest, 'current_test_failed') and pytest.current_test_failed:
        # Get timestamped results directory
        config = request.config
        if hasattr(config, 'results_dir'):
            screenshot_dir = config.results_dir / "screenshots"
        else:
            # Fallback if results_dir not set
            screenshot_dir = Path("./results_Playwright/screenshots")
        
        # Create screenshots directory
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Create timestamped screenshot filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name[:50]  # Limit length
        screenshot_path = screenshot_dir / f"failure_{test_name}_{timestamp}.png"
        
        # Take screenshot
        try:
            page.screenshot(path=str(screenshot_path))
            print(f"📸 Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"⚠️  Failed to capture screenshot: {e}")


# ============================================================================
# FIXTURES - CUSTOM (Add your project-specific fixtures here)
# ============================================================================

# Example: Page Object Fixtures
# Uncomment and modify as needed for your project

# @pytest.fixture
# def login_page(page):
#     """
#     Provides LoginPage instance
#     
#     Usage in tests:
#         def test_login(login_page):
#             login_page.navigate()
#             login_page.login("user", "pass")
#     """
#     from pages.login_page import LoginPage
#     return LoginPage(page)


# @pytest.fixture
# def home_page_obj(page):
#     """
#     Provides HomePage instance
#     
#     Usage in tests:
#         def test_search(home_page_obj):
#             home_page_obj.navigate()
#             home_page_obj.search("product")
#     """
#     from pages.home_page_obj import HomePage
#     return HomePage(page)


# Example: Authenticated User Fixture
# @pytest.fixture
# def auth_page(page):
#     """
#     Provides a page with user already logged in
#     
#     Usage in tests:
#         def test_profile(auth_page):
#             # User is already logged in!
#             auth_page.goto("/profile")
#     """
#     from pages.login_page import LoginPage
#     from config.config import Config
#     
#     login_page = LoginPage(page)
#     login_page.navigate()
#     
#     creds = Config.get_valid_credentials()
#     login_page.login(creds["email"], creds["password"])
#     
#     return page


# Example: Test Data Fixtures
# @pytest.fixture
# def valid_user():
#     """
#     Returns valid user credentials
#     
#     Usage in tests:
#         def test_login(login_page, valid_user):
#             login_page.login(valid_user["email"], valid_user["password"])
#     """
#     from config.config import Config
#     return Config.get_valid_credentials()


# @pytest.fixture
# def invalid_user():
#     """Returns invalid user credentials for negative tests"""
#     return {
#         "email": "invalid@example.com",
#         "password": "wrongpassword"
#     }


# ============================================================================
# UTILITY FUNCTIONS (Helper functions for tests)
# ============================================================================

def log_step(message: str):
    """
    Log a test step with emoji
    
    Usage in tests:
        log_step("Navigating to login page")
        log_step("Filling username field")
    """
    logger = logging.getLogger(__name__)
    logger.info(f"🔹 {message}")


def log_action(message: str):
    """
    Log a user action with emoji
    
    Usage in tests:
        log_action("Click login button")
        log_action("Type 'test@example.com' in email field")
    """
    logger = logging.getLogger(__name__)
    logger.info(f"👉 {message}")


def log_verification(message: str):
    """
    Log a verification/assertion with emoji
    
    Usage in tests:
        log_verification("Login successful")
        log_verification("Error message displayed")
    """
    logger = logging.getLogger(__name__)
    logger.info(f"✓ {message}")


# ============================================================================
# CONFIGURATION SUMMARY
# ============================================================================
"""
This conftest.py provides:

✅ Timestamped Results
   - Each test run gets its own folder
   - Complete test history preserved
   - Easy to compare results over time

✅ Beautiful Console Output
   - Test start banners with timestamps
   - Clear PASS/FAIL/SKIP indicators
   - Test duration displayed

✅ Automatic Screenshots
   - Captured on test failure only
   - Saved to timestamped results folder
   - Filename includes test name and timestamp

✅ Automatic Cleanup
   - Removes invalid video metadata files
   - Keeps results folder clean

✅ Works From Anywhere
   - Results always go to project root
   - Doesn't matter where you run pytest

✅ Easy to Customize
   - Add your own fixtures
   - Modify logging functions
   - Extend hooks as needed

To use in tests:
    1. Page fixture available automatically (from pytest-playwright)
    2. Add your custom fixtures in "FIXTURES - CUSTOM" section
    3. Use log_step(), log_action(), log_verification() for better logs
"""


'''
# This is the "Professional" way to load fixtures from other folders
# effectively treating them as plugins.
pytest_plugins = [
    "fixtures.page_fixtures",
    # You can add "fixtures.api_fixtures" here later
]
'''


# Add to your existing conftest.py for test_site_health.py and test_quick_scan.py

@pytest.fixture(scope="session")
def browser(browser_type):
    """Browser instance for tests"""
    browser = browser_type.launch(headless=False, slow_mo=500)
    yield browser
    browser.close()