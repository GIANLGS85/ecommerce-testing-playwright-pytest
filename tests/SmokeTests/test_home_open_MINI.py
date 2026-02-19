import re
from playwright.sync_api import expect
from pages.home_page import HomePage

def test_home_page_loads(home_page_obj: HomePage):
    expect(home_page_obj.page).to_have_title(re.compile('.*Practice Software Testing.*'))
