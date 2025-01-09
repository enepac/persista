import unittest
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.src.main import app

class HealthEndpointTest(unittest.TestCase):
    def setUp(self):
        # Create a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        # Send a GET request to the /health endpoint
        response = self.app.get('/health')
        # Assert the status code is 200
        self.assertEqual(response.status_code, 200)
        # Assert the response JSON matches the expected output
        self.assertEqual(response.json, {"status": "healthy"})

if __name__ == '__main__':
    unittest.main()
