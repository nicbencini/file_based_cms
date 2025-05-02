import unittest
import os
from src.file_based_cms import app
from pathlib import Path

class AppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_index(self):
        with self.client.get('/') as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/html; charset=utf-8")
            self.assertIn("about.txt", response.get_data(as_text=True))
            self.assertIn("changes.txt", response.get_data(as_text=True))
            self.assertIn("history.txt", response.get_data(as_text=True))
            self.assertIn("markd.md", response.get_data(as_text=True))

    def test_viewing_text_document(self):
        with self.client.get('/history.txt') as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/html; charset=utf-8")
            self.assertIn("Python 0.9.0 (initial release) is released.",
                        response.get_data(as_text=True))

    def test_file_not_found(self):
        with self.client.get('/xxx') as response:
            self.assertEqual(response.status_code, 302)
    
    def test_viewing_markdown_document(self):
        response = self.client.get('/about.md')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
        #self.assertIn("<h1>Python is...</h1>", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
