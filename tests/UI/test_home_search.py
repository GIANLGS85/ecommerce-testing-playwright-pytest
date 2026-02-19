from playwright.sync_api import Page, expect
from pages.home_page import HomePage
import logging 

logger = logging.getLogger(__name__)

def test_search_returns_results_for_valid_term(home_page_obj: HomePage):
    '''
    Search for "hammer"
    Assert at least 1 product is shown
    '''
    
    print("Actual object type:", type(home_page_obj)) 
    print("HomePage class file:", home_page_obj.__class__.__module__) 
    print("Methods in object:", dir(home_page_obj))

    logger.info(f"Actual object type: {type(home_page_obj)}")
    logger.info(f"HomePage class file: {home_page_obj.__class__.__module__}") 
    logger.info(f"Methods in object: {dir(home_page_obj)}")
    
    home_page_obj.search_for_product("hammer")
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)

    

def test_search_no_results_for_gibberish(home_page_obj: HomePage):
    '''
    Search for "asdasdasd123"
    Assert “no results” message OR zero products
    '''
    home_page_obj.search_for_product("asdasdasd123")
    
    # Assert “no results” message
    expect(home_page_obj.locators.no_results_message).to_be_visible()
    
    # Zero products
    expect(home_page_obj.locators.product_cards).to_have_count(0)
    
    
def test_search_clearing_input_restores_products(home_page_obj: HomePage):
    '''
    Search somethingtest_search_clearing_input_restores_products
    Clear input
    Assert products reappear
    '''
    initial_count = home_page_obj.get_collection_count_safe(locator=home_page_obj.locators.product_cards, minimum=1)
    logger.info(f"initial_count = {initial_count}")

    home_page_obj.search_for_product(product_name="hammer")
    expect(home_page_obj.locators.product_cards.first).to_be_visible()

    filtered_count = home_page_obj.get_collection_count_safe(locator=home_page_obj.locators.product_cards, minimum=1)
    logger.info(f"There are {filtered_count} products found after reset search")
    assert filtered_count < initial_count

    home_page_obj.locators.search_reset_button.click()
    # Reset is expected to restore the original count
    expect(home_page_obj.locators.product_cards).to_have_count(initial_count)
    logger.info(f"There are {home_page_obj.locators.product_cards.count()} products found after reset search")
    
    
    
    
    
