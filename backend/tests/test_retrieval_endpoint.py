import unittest
from backend.src.main import app  # Adjust the import path to your actual app entry point

class RetrievalEndpointTest(unittest.TestCase):
    def setUp(self):
        # Create a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

    def test_retrieve_valid_project(self):
        # Simulate a valid retrieval request
        payload = {"project_id": "12345", "query": "example file"}
        
        # Send a POST request to the /retrieve endpoint
        response = self.app.post('/retrieve', json=payload)
        
        # Assert the status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Assert the response contains expected data
        expected_response = {
            "success": True,
            "files": [
                {"file_name": "example.txt", "file_path": "/project-workspaces/12345/example.txt"}
            ]
        }
        self.assertEqual(response.json, expected_response)

    def test_retrieve_invalid_project(self):
        # Simulate a request for a non-existent project
        payload = {"project_id": "99999", "query": "nonexistent file"}
        
        # Send a POST request to the /retrieve endpoint
        response = self.app.post('/retrieve', json=payload)
        
        # Assert the status code is 404 (not found)
        self.assertEqual(response.status_code, 404)
        
        # Assert the response indicates failure
        self.assertIn("error", response.json)

if __name__ == '__main__':
    unittest.main()
