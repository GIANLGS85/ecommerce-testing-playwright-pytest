import re
import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
import logging 

logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("delete_store_state")
def test_home_login_link_navigates_to_login(home_page_obj: HomePage):
    '''
    Click “Login”
    Assert URL contains /login
    '''

    home_page_obj.locators.signin_link.click()
    # ✅ Use BasePage method for assertion
    home_page_obj.assert_url_contains("/auth/login")
    

def test_login_page_register_link_navigates_to_register(home_page_obj: HomePage):
    '''
    Click “Register”
    Assert URL contains /register
    '''
    
    # Click Signin link
    home_page_obj.locators.signin_link.click()
    
    home_page_obj.assert_url_contains("/auth/login")
    
    # Click Register link
    home_page_obj.locators.register_link.click()
    
    # Assert navigation to register page
    home_page_obj.assert_url_contains("/auth/register")
    


def test_home_cart_link_opens_cart(home_page_obj: HomePage):
    '''
    Click cart icon/link
    Assert URL contains /cart
    '''
    
    # Open first product from the grid (generic, stable)
    home_page_obj.locators.first_product.click()
    
    # Add product to cart: Click add-to-cart button 
    home_page_obj.locators.add_to_cart_button.click()

    # Click cart icon/link
    home_page_obj.locators.cart_icon.click()
    
    expect(home_page_obj.page).to_have_url(re.compile(".*/checkout")) #https://practicesoftwaretesting.com/checkout
    

def test_clicking_product_opens_product_detail(home_page_obj: HomePage):
    '''
    Click first product
    Assert URL contains /product
    Assert product title is visible
    '''
    # Click on the first product in the grid
    home_page_obj.locators.product_cards.first.click()
    
    # Assert navigation to a product detail page
    expect(home_page_obj.page).to_have_url(re.compile('.*/product/.+'))
    
    # Assert product title is visible
    expect(home_page_obj.locators.product_name).to_be_visible()
    