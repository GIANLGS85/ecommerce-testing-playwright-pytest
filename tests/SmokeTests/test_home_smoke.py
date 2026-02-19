import re
from playwright.sync_api import expect
from pages.home_page import HomePage
import logging 

logger = logging.getLogger(__name__)

def test_home_page_loads(home_page_obj: HomePage):
    '''
    Go to /
    Assert page title contains “Practice Software Testing”

    '''
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)
    expect(home_page_obj.page).to_have_title(re.compile(".*Practice Software Testing"))
    
    
def test_home_products_are_visible(home_page_obj: HomePage):
    '''
    Assert product grid/list is visible
    Assert at least 1 product card exists
    '''
    
    # 1️⃣ Assert product grid/list container is visible
    # Because There is NO stable data-test for the product list container, we must use this:
    expect(home_page_obj.locators.product_cards.first).to_be_visible()

    # 2️⃣ Assert at least one product card exists
    # Because The data-test on products is dynamic (IDs change), we must use this:
    expect(home_page_obj.locators.product_cards).not_to_have_count(0)

    
def test_home_header_is_visible(home_page_obj: HomePage):   
    '''
    Assert header/navbar is visible
    '''
    # Assert the navbar container is visible
    expect(home_page_obj.locators.navbar).to_be_visible()
    
    
def test_home_footer_is_visible(home_page_obj: HomePage):
    '''
    Assert footer is visible
    ''' 
    expect(home_page_obj.locators.footer).to_be_visible()