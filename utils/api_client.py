import logging
from typing import Dict, Optional, Any
from config.config import Config
from playwright.sync_api import APIRequestContext, APIResponse


class APIClient:
    """
    Unified API Client using Playwright's APIRequestContext.
    Provides centralized logging and error handling for all HTTP methods.
    """

    def __init__(self, request_context: APIRequestContext):
        self.request = request_context
        # Centralized base URL for the project
        self.api_base_url = Config.API_BASE_URL
        self.logger = logging.getLogger(__name__)

    def _execute_request(self, method: str, endpoint: str, **kwargs) -> APIResponse:
        """
        Internal wrapper to execute requests with logging.
        """
        url = f"{self.api_base_url}{endpoint}" if endpoint.startswith("/") else endpoint
        self.logger.info(f"Sending {method.upper()} to {url}")

        # Mapping string methods to Playwright's request object
        # kwargs can include: data, params, headers, etc.
        response = self.request.fetch(url, method=method, **kwargs)

        return response

    # ========================================================================
    # PUBLIC API METHODS
    # ========================================================================

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Standard GET request."""
        return self._execute_request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Standard POST request."""
        return self._execute_request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Standard PUT request."""
        return self._execute_request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> APIResponse:
        """Standard DELETE request."""
        return self._execute_request("DELETE", endpoint)

    # ========================================================================
    # DOMAIN SPECIFIC METHODS (Convenience)
    # ========================================================================

    def get_brands(self) -> APIResponse:
        """Fetch all brands from the backend."""
        return self.get("/brands")

    def get_products(self, params: Dict[str, Any]) -> APIResponse:
        """Fetch products with optional filters (page, price between, is_rental)."""
        return self.get("/products", params=params)

    def create_contact_message(self, payload: Dict[str, Any]) -> APIResponse:
        """Example of a POST request to a specific endpoint."""
        return self.post("/contact/send", data=payload)