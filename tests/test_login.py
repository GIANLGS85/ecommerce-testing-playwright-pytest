from playwright.sync_api import expect
from config.config import Config


def test_login_page(user_page) -> None:
    user_page.goto(Config.LOGIN_URL)
    expect(user_page.locator('[data-test="page-title"]')).to_have_text("My account")
    #expect(user_page.get_by_label("Page context").locator("span")).to_have_text("My Account")


