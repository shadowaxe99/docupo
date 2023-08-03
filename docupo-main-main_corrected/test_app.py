from ctypes.wintypes import tagSIZE
import unittest
import requests

class TestApp(unittest.TestCase):
    BASE_URL = 'http://localhost:5000'

    def test_upload_document(self):
        # Test successful document upload
        with open('AGENTS.pdf', 'rb') as f:
            response = requests.post(self.BASE_URL + '/upload', files={'document': f})
            self.assertEqual(response.status_code, 200)

        # Test upload with invalid file format
        with open('invalid_file.jpg', 'rb') as f:
            response = requests.post(self.BASE_URL + '/upload', files={'document': f})
            self.assertEqual(response.status_code, 400)

        # Test upload with file that causes error during document processing
        with open('error_file.txt', 'rb') as f:
            response = requests.post(self.BASE_URL + '/upload', files={'document': f})
            self.assertEqual(response.status_code, 500)

    def test_review_repo_structure(self):
        # Test successful repository creation
        repo_structure = {'repo_structure': 'dummy_repo_structure'}
        response = requests.post(self.BASE_URL + '/review', json=repo_structure)
        self.assertEqual(response.status_code, 200)

        # Test review with invalid repository structure
        invalid_repo_structure = {'repo_structure': None}
        response = requests.post(self.BASE_URL + '/review', json=invalid_repo_structure)
        self.assertEqual(response.status_code, 400)

        # Test review that causes error during repository creation
        error_repo_structure = {'repo_structure': 'error_repo_structure'}
        response = requests.post(self.BASE_URL + '/review', json=error_repo_structure)
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
