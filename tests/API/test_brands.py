import logging
from playwright.sync_api import expect

logger = logging.getLogger(__name__)


def test_should_retrieve_at_least_two_brands(api_client):
    # Act: Use the client helper
    response = api_client.get_brands()

    # Assert: Use Playwright 'expect' for the response
    expect(response).to_be_ok()

    # Assert: Validate at least 2 brands are returned
    data = response.json()
    found_brands = len(data)
    logger.info(f"Brands found: {found_brands}")
    assert found_brands >= 2

