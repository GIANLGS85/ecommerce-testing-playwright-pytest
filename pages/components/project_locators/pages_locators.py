from playwright.sync_api import Page


class LoginPageLocators:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator('[data-test="email"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button_text = page.locator('[data-test="login-submit"]')

        self.login_button_type_submit = page.locator("input[type='submit']")
        self.error_message = page.locator("div.flash.error")
        self.page_title = page.locator('[data-test="page-title"]')


class HomePageLocators:
    def __init__(self, page: Page):
        self.page = page
        # ===== HomePage locators =====
        # HEADER / NAVIGATION LOCATORS
        self.logo = page.locator('[data-test="nav-logo"]')
        self.signin_link = page.locator('[data-test="nav-sign-in"]')
        self.register_link = page.locator('[data-test=\"register-link\"]')
        self.cart_icon = page.locator('[data-test="nav-cart"]')
        self.cart_count_badge = page.locator('[data-test="cart-quantity"]')
        self.user_menu = page.locator('[data-test="nav-user-menu"]')
        self.active_page_number = page.locator("li.page-item.active a[role='button']")

        # SORTING & PAGINATION LOCATORS
        self.sort_dropdown = page.locator('[data-test="sort"]')
        self.pagination = page.locator(".pagination")
        self.next_page_button = page.locator('[aria-label="Next"]')
        self.prev_page_button = page.locator('[aria-label="Previous"]')

        # PRICE RANGE LOCATORS
        self.slider_min = page.get_by_role("slider", name="ngx-slider")
        self.slider_max = page.get_by_role("slider", name="ngx-slider-max")
        self.slider_text_1 = page.locator("#filters").get_by_text("1")
        self.slider_text_200 = page.get_by_text("200").nth(1)

        # SEARCH BAR LOCATORS
        self.search_input = page.locator('[data-test="search-query"]')
        self.search_submit_button = page.locator('[data-test="search-submit"]')
        self.search_reset_button = page.locator('[data-test="search-reset"]')
        self.search_suggestions = page.locator('[data-test="search-suggestions"]')
        self.search_term = page.locator("[data-test=\"search-term\"]")

        # FILTER SIDEBAR LOCATORS
        self.category_checkboxes = page.locator("input[name='category_id']")
        self.brand_checkboxes = page.locator("input[name='brand_id']")
        self.price_min_input = page.locator('[data-test="price-min"]')
        self.price_max_input = page.locator('[data-test="price-max"]')
        self.price_apply_button = page.locator('[data-test="price-apply"]')
        self.reset_filters_button = page.locator('[data-test="reset-filters"]')

        # PRODUCT GRID LOCATORS
        self.products_container = page.locator("div.col-md-9")
        self.product_cards = page.locator("a.card[href^='/product/']")
        self.first_product = page.locator("a.card[href^='/product/']").first
        self.product_name = page.locator('[data-test="product-name"]')
        self.product_prices = page.locator('[data-test="product-price"]')
        self.product_images = page.locator('[data-test="product-image"]')
        self.no_results_message = page.locator('[data-test="no-results"]')
        self.add_to_cart_button = page.locator('[data-test="add-to-cart"]')
        self.product_in_cart = page.locator("span[data-test='product-title']")

        # FOOTER LOCATORS
        self.footer = page.locator("app-footer")
        self.footer_privacy_link = page.locator("footer a[href*='privacy']")
        self.footer_terms_link = page.locator("footer a[href*='terms']")
        self.footer_contact_link = page.locator("footer a[href*='contact']")

        # PAGE STRUCTURE LOCATORS
        self.navbar = page.locator("nav.navbar")
        self.hero_section = page.locator(".hero-section")

class ProductDetailsPageLocators:
    def __init__(self, page: Page):
        self.page = page

        # ===== Product Header & Price =====
        self.product_name = page.locator('[data-test="product-name"]')
        self.unit_price = page.locator('[data-test="unit-price"]')
        self.product_description = page.locator('[data-test="product-description"]')

        # ===== Quantity & Cart =====
        self.quantity_input = page.locator('[data-test="quantity"]')
        self.increase_quantity_btn = page.locator('[data-test="increase-quantity"]')
        self.decrease_quantity_btn = page.locator('[data-test="decrease-quantity"]')
        self.add_to_cart_btn = page.locator('[data-test="add-to-cart"]')

        # ===== Status & Metadata =====
        self.out_of_stock_message = page.get_by_text("Out of stock")
        self.is_rental_badge = page.locator('.badge', has_text="Rental")

        # ===== Image & Category Info =====
        self.product_image = page.locator('img.figure-img')
        self.category_breadcrumb = page.locator('ol.breadcrumb')  # Common path for categories

        # ===== Global Header Elements (Inherited context) =====
        self.cart_badge = page.locator('[data-test="cart-quantity"]')

class CartPageLocators:
    def __init__(self, page: Page):
        self.page = page

        # ===== Table / Item Row Locators =====
        # This identifies the rows in the cart table
        self.cart_items = page.locator('tr')
        self.cart_icon = page.locator('[data-test="nav-cart"]')
        self.total_price_text = page.locator('[data-test="cart-total"]')

        # Specific item details (usually found within a row)
        self.product_title = page.locator('[data-test="product-title"]')
        self.product_price = page.locator('[data-test="product-price"]')
        self.line_total = page.locator('[data-test="line-price"]')

        # ===== Quantity Controls (Inside the Cart) =====
        self.quantity_input = page.locator('[data-test="quantity"]')

        # ===== Totals & Summary =====
        self.total_price = page.locator('[data-test="cart-total]')
        self.checkout_button = page.locator('[data-test="proceed-1"]')

        # ===== Delete/Remove =====
        # Finding the delete button for a specific item
        self.delete_button = page.locator('a.btn-danger')

        # ===== Navigation / Stepper (The Checkout Process) =====
        # The checkout page uses a multi-step wizard (Stepper)
        self.stepper_cart = page.locator('app-checkout')
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')

        self.search_input = page.get_by_placeholder("Search products...")
        self.search_btn = page.get_by_role("button", name="Search")
        self.add_to_cart_btn = page.get_by_role("button", name="Add to Cart")
        self.cart_icon = page.locator(".cart-icon")
        self.checkout_btn = page.get_by_role("button", name="Proceed to Checkout")
