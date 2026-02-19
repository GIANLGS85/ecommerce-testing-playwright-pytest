from playwright.sync_api import Page

class FilterLocators:
    def __init__(self, page: Page):
        self.page = page
        # ===== Filters locators =====
        self.price_apply_btn = page.locator('[data-test="price-apply"]')
        self.reset_filters_btn = page.locator('[data-test="reset-filters"]')
        self.active_filters = page.locator('[data-test="active-filter"]')
        self.category_id = page.locator("input[name='category_id']")
        self.brand_id = page.locator("input[name='brand_id']")
        self.price_min = page.locator('[data-test="price-min"]')
        self.price_max = page.locator('[data-test="price-max"]')


class HeaderLocators:
    def __init__(self, page: Page):
        self.page = page
        # ===== Headers locators =====
        self.logo = page.locator('[data-test="nav-logo"]')
        self.cart_icon = page.locator('[data-test="nav-cart"]')
        self.cart_count_badge = page.locator('[data-test="cart-quantity"]')
        self.user_menu = page.locator('[data-test="nav-user-menu"]')
        self.login_link = page.locator('[data-test="nav-sign-in"]')
        self.logout_button = page.locator('[data-test="nav-sign-out"]')
        self.category_links = page.locator("nav a[href*='category']")


class PaginationLocators:
    def __init__(self, page: Page):
        self.page = page
        # ===== Pagination Locators =====
        self.pagination_container = page.locator(".pagination")
        self.page_buttons = page.locator(".pagination a")
        self.next_button = page.locator('[aria-label="Next"]')
        self.prev_button = page.locator('[aria-label="Previous"]')
        self.current_page_indicator = page.locator(".pagination .active")


class ProductGridLocators:
    def __init__(self, page: Page):
        self.page = page
        # ===== Product Grid Locators =====
        self.product_cards = page.locator("a.card[href^='/product/']")
        self.product_names = page.locator('[data-test="product-name"]')
        self.product_prices = page.locator('[data-test="product-price"]')
        self.product_images = page.locator('[data-test="product-image"]')
        self.sort_dropdown = page.locator('[data-test="sort"]')
        self.no_results_message = page.locator('[data-test="no-results"]')


class SearchBarLocators:
    def __init__(self, page: Page):
        self.page = page
        # ===== Search bar locators =====
        self.search_input = page.locator('[data-test="search-query"]')
        self.search_button = page.locator('[data-test="search-submit"]')
        self.search_reset = page.locator('[data-test="search-reset"]')
        self.search_suggestions = page.locator('[data-test="search-suggestions"]')

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
        self.product_names = page.locator('[data-test="product-name"]')
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



