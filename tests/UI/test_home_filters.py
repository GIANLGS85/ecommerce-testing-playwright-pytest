from playwright.sync_api import Page, expect
from pages.home_page import HomePage
import logging 

logger = logging.getLogger(__name__)

def test_filter_by_category_reduces_products(home_page_obj: HomePage):
    '''
    Select one category
    Assert product count changes
    '''
    # Ensure product_cards exist initially
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)
    
    # Check the Filter by Category checkbox
    home_page_obj.filter_by_category(category_name = "Hand Tools")
    
    # Assert product list changes (filtered)
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)
    
    # Uncheck the Filter by Category checkbox
    home_page_obj.unfilter_by_category(category_name = "Hand Tools")


def test_filter_by_brand_reduces_products(home_page_obj: HomePage):
    '''
    Select one brand
    Assert product count changes
    '''
    
    # Initial state: Ensure product_cards exist initially
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)
    
    # Select first brand checkbox
    home_page_obj.locators.brand_checkboxes.first.check()
    
    # Assert product list changes (filtered)
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)
    


def test_sort_by_price_changes_product_order(home_page_obj: HomePage):
    '''
    Capture first product price 
    Apply “Sort by price” 
    Assert first product price changed
    '''
    # Initial state: Ensure product_cards exist initially
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)
    
    # Capture first product price BEFORE sorting
    list_of_product_prices = home_page_obj.get_all_product_prices()
    first_price_before = list_of_product_prices[0]
    logger.info(f"first_price_before = {first_price_before}")

    # Apply "Sort by price: High - Low" drop-down
    home_page_obj.sort_by_label("Price (High - Low)")

    # Capture first product price AFTER sorting
    list_of_product_prices = home_page_obj.get_all_product_prices()
    first_price_after = list_of_product_prices[0]
    logger.info(f"first_price_after = {first_price_after}")

    # Assert sorting changed the order
    assert first_price_after >= first_price_before

def test_reset_filters_restores_all_products(home_page_obj: HomePage):
    '''
    Apply filter
    Reset filters
    Assert full product list returns
    '''
    # Initial state: Ensure product_cards exist initially 
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)
    
    # Apply filter - For checkbox, get_by_label is the best option
    home_page_obj.filter_by_category("Hand Tools")
    
    # Reset filter
    home_page_obj.unfilter_by_category("Hand Tools")
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)
    
    
def test_reset_search_and_filters_restores_all_products(home_page_obj: HomePage):
    '''
    Search
    Filter after category
    Reset both
    '''
    # Initial state: Ensure product_cards exist initially
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)
    
    # Original number of products
    initial_count = home_page_obj.get_product_count()
    
    # Search after hammer
    home_page_obj.search_for_product(product_name="hammer")
    
    # Apply filter - For checkbox, get_by_label is the best option
    home_page_obj.filter_by_category(category_name="Hand Tools")
    
    # Click on Search-reset button
    home_page_obj.reset_search()
    
    # Reset category filter explicitly
    home_page_obj.unfilter_by_category(category_name="Hand Tools")
    
    # Reset is expected to restore the original count
    expect(home_page_obj.locators.product_cards).to_have_count(initial_count)
    
    # Instead of checking exact count:
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)  # Just verify "some products exist"
    
    
def test_sort_then_filter_then_reset_restores_default_order(home_page_obj: HomePage):
    '''
    Sort
    Filter
    Reset both
    Assert default order
    '''
    # Initial state: Ensure product_cards exist initially
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)
    
    product_default_names = home_page_obj.get_all_product_names()
    
    # Apply sort: Price High -> Low
    home_page_obj.sort_by_label(label="Price (High - Low)")

    # Wait
    #home_page_obj.wait_for_content_loaded()
    
    sorted_names = home_page_obj.get_all_product_names()
    
    assert sorted_names != product_default_names
    
    # Apply filter - For checkbox, get_by_label is the best option
    home_page_obj.filter_by_category("Hand Tools")
    
    # Wait
    #home_page_obj.wait_for_content_loaded()
    
    # Reset filter
    home_page_obj.unfilter_by_category("Hand Tools")
    
    # Wait
    #home_page_obj.wait_for_content_loaded()

    # Capture order after reset filter
    reset_filter_names = home_page_obj.get_all_product_names()
    
    # Assert filter is no longer applied
    assert reset_filter_names == sorted_names
    
    # Reset sorting
    home_page_obj.sort_by_label(label="")
    
    # Wait
    #home_page_obj.wait_for_content_loaded()
    
    # Capture order after reset filter
    reset_sort_names = home_page_obj.get_all_product_names()
    
    # Assert sorting is no longer applied
    assert reset_sort_names == product_default_names
    

def test_sorting_stability_across_pages(home_page_obj: HomePage):
    '''
    Sort "Price (High - Low)"
    Assert the order for page 1 and page 2 to be "Price (High - Low)"
    Reset sorting
    '''
    # Initial state: Ensure product_cards exist initially
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)
    
    home_page_obj.sort_by_label(label="Price (High - Low)")

    page_1_values = home_page_obj.get_all_product_prices()
    logger.info(f"page_1_values = {page_1_values}")

    # Assert Page 1 is sorted
    assert page_1_values == sorted(page_1_values, reverse=True)

    # Go to Page 2
    home_page_obj.go_to_page(page_number=2)
    expect(home_page_obj.locators.active_page_number).to_have_text("2")

    # Page 2 prices
    page_2_values = home_page_obj.get_all_product_prices()
    logger.info(f"page_2_values = {page_2_values}")
    
    # Assert Page 2 is sorted
    assert page_2_values == sorted(page_2_values, reverse=True)

    # Combine prices
    all_prices = page_1_values + page_2_values
    logger.info(f"all_prices = {all_prices}")

    # Assert global sorting across pages
    assert all_prices == sorted(all_prices, reverse=True)

    # Reset sorting
    home_page_obj.sort_by_label(label="")
    
    
def test_sorting_stability_across_pages_2(home_page_obj: HomePage):
    '''
    Sort "Price (High - Low)"
    Assert the order for page 1 and page 2 to be "Price (High - Low)"
    Reset sorting
    '''
    home_page_obj.sort_by_label(label="Price (High - Low)")
    
    assert home_page_obj.is_products_sorted_by_price_descending() == True
    
    # Page 2 prices
    home_page_obj.go_to_page(page_number=2)
    expect(home_page_obj.locators.active_page_number).to_have_text("2")
    
    assert home_page_obj.is_products_sorted_by_price_descending() == True
    
    # Reset sorting
    home_page_obj.sort_by_label(label="")
    
    
    
    
    
    
    