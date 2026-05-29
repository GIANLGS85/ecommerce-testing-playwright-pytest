import os

class Config:

    # ============================================================================
    # ENVIRONMENT DETECTION
    # ============================================================================
    CI_MODE = os.getenv("CI") == "true"

    # Load credentials from environment variables (fallback to demo defaults)
    # https://testsmith-io.github.io/practice-software-testing/#/
    # for testing purposes using default user as mentioned in the official website
    TEST_USER = "customer@practicesoftwaretesting.com"
    TEST_PWD = "welcome01" #os.getenv("TEST_PWD", "welcome01")

    # Browser Settings
    # Determines if the browser should run without a GUI (Headless mode)
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

    # ============================================================================
    # CLOUDFLARE PROTECTION - CI/CD SPECIFIC HANDLING
    # ============================================================================
    # In CI environment, Cloudflare needs 20-45+ seconds to verify browser
    # Locally 10-20 secondi bastano
    if CI_MODE:
        CLOUDFLARE_TIMEOUT = int(os.getenv("CLOUDFLARE_TIMEOUT", "45000"))  # 45s in CI
        CLOUDFLARE_RETRY_COUNT = int(os.getenv("CLOUDFLARE_RETRY_COUNT", "3"))
        CLOUDFLARE_RETRY_DELAY = int(os.getenv("CLOUDFLARE_RETRY_DELAY", "3000"))  # 3s between retries
    else:
        CLOUDFLARE_TIMEOUT = int(os.getenv("CLOUDFLARE_TIMEOUT", "20000"))  # 20s locally
        CLOUDFLARE_RETRY_COUNT = 1
        CLOUDFLARE_RETRY_DELAY = 1000

    # Global explicit timeout in milliseconds (Replaces hard-coded sleep)
    DEFAULT_TIMEOUT = 10000

    # Environment URLs
    BASE_URL = os.getenv("BASE_URL", "https://practicesoftwaretesting.com/")
    if not BASE_URL:
        raise RuntimeError("BASE_URL is not set")

    # Login URL
    LOGIN_URL = os.getenv("LOGIN_URL", BASE_URL+"auth/login")
    if not LOGIN_URL:
        raise RuntimeError("LOGIN_URL is not set")

    # After Login URL
    AFTER_LOGIN_URL = os.getenv("AFTER_LOGIN_URL", BASE_URL+"account")
    if not AFTER_LOGIN_URL:
        raise RuntimeError("AFTER_LOGIN_URL is not set")

    # API Base url
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.practicesoftwaretesting.com")
    if not API_BASE_URL:
        raise RuntimeError("API_BASE_URL is not set")

    # Timeouts
    DEFAULT_TIMEOUT = int(os.getenv("TIMEOUT", 10000))
