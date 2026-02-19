import pytest
import logging
from playwright.sync_api import expect

logger = logging.getLogger(__name__)

def test_should_filter_products_by_price_and_rental_status(api_client):
    # 1. Arrange: Define the filters
    params = {
        "page": 1,
        "between": "price,1,100",
        "is_rental": "false"
    }

    # 2. Act: Call the API
    response = api_client.get_products(params)

    # 3. Assert: Network level validation
    expect(response).to_be_ok()

    # 4. Assert: Data level validation
    payload = response.json()
    products = payload.get("data", [])

    # Check that we actually got items
    assert len(products) > 0, "No products returned for the specified filters"

    # Validate the first item respects the filters
    first_product = products[0]

    # Check Price (Should be between 1 and 100)
    product_price = first_product["price"]
    assert 1 <= product_price <= 100, f"Product price {product_price} is out of range!"

    # Check Rental Status (Should be False)
    assert first_product["is_rental"] is False, "Product should not be a rental"

    # Log results for the report
    logger.info(f"Verified {len(products)} products. First item: {first_product['name']} at ${product_price}")