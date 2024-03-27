import unittest
import json
import sys
import os

# This allows for importing modules from the parent directory. It is done just for the purpose of running this test.
# Usually this is handled by test frameworks, but for the current scenario, we can go with the following.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fee_calculator.app import app


class TestItemMethods(unittest.TestCase):
    """
    Test suite for item-related API endpoints in the Flask application.

    Methods:
        setUp: Prepares the test client for the application.
        test_valid_input: Tests the API endpoint with valid input data.
        test_invalid_input: Tests the API endpoint with invalid input data.
        test_missing_input: Tests the API endpoint with missing fields in input data.
        test_missing_invalid_input: Tests the API endpoint with missing fields and invalid input data.
    """

    def setUp(self):
        """
        Set up method to initialize a test client for the Flask application.
        This method is called before each test.
        """
        self.app = app.test_client()

    def test_valid_input(self):
        """
        Test case for verifying the API's response to valid input.

        This method sends a POST request with valid item details and
        checks for a successful response (status code 200) and
        the presence of a 'delivery_fee' in the response data.
        """
        response = self.app.post(
            "/",
            json={
                "cart_value": 1500,
                "delivery_distance": 1000,
                "number_of_items": 3,
                "time": "2024-01-26T15:00:00",
            },
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("delivery_fee", response_data)

    def test_invalid_input(self):
        """
        Test case for verifying the API's response to invalid input.

        This method sends a POST request with invalid item details and
        checks for an error response (status code 400).
        """
        response = self.app.post(
            "/",
            json={
                "cart_value": "1500",
                "delivery_distance": -1,
                "number_of_items": 0,
                "time": "2024-01-36T15:00:00",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_missing_input(self):
        """
        Test case for verifying the API's response to missing fields in the input.

        This method sends a POST request with missing fields and
        checks for an error response (status code 400).
        """
        response = self.app.post(
            "/",
            json={
                "delivery_distance": 1000,
                "number_of_items": 8,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_missing_invalid_input(self):
        """
        Test case for verifying the API's response to missing and invalid fields in the input.

        This method sends a POST request with missing fields and
        checks for an error response (status code 400).
        """
        response = self.app.post(
            "/",
            json={
                "delivery_distance": -1,
                "number_of_items": 8,
            },
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
