import unittest
import os
from src.file_based_cms import app
from pathlib import Path
import shutil
import os

class AppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.data_path = os.path.join(os.path.dirname(__file__))
        os.makedirs(self.data_path, exist_ok=True)
    
    def test_index(self):
        self.create_document("about.md")
        self.create_document("changes.txt")

        with self.client.get('/') as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/html; charset=utf-8")
            self.assertIn("about.txt", response.get_data(as_text=True))
            self.assertIn("changes.txt", response.get_data(as_text=True))
            self.assertIn("history.txt", response.get_data(as_text=True))
            self.assertIn("markd.md", response.get_data(as_text=True))

    def test_viewing_text_document(self):
        self.create_document("history.txt")
        with self.client.get('/history.txt') as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/html; charset=utf-8")
            self.assertIn("Python 0.9.0 (initial release) is released.",
                        response.get_data(as_text=True))

    def test_file_not_found(self):
        with self.client.get('/xxx') as response:
            self.assertEqual(response.status_code, 302)
    
    def test_viewing_markdown_document(self):
        self.create_document("about.md")
        response = self.client.get('/about.md')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
        #self.assertIn("<h1>Python is...</h1>", response.get_data(as_text=True))


    def test_editing_document(self):
        self.create_document("changes.txt")

        response = self.client.get("/changes.txt/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn("<textarea", response.get_data(as_text=True))
        self.assertIn('<button type="submit"', response.get_data(as_text=True))

    def test_updating_document(self):
        self.create_document("changes.txt")
        response = self.client.post("/changes.txt",
                                    data={'file_contents': "new content"})
        self.assertEqual(response.status_code, 302)

        follow_response = self.client.get(response.headers['Location'])
        self.assertIn("changes.txt has been updated",
                      follow_response.get_data(as_text=True))

        with self.client.get("/changes.txt") as content_response:
            self.assertEqual(content_response.status_code, 200)
            self.assertIn("new content",
                          content_response.get_data(as_text=True))
    
    def tearDown(self):
        #shutil.rmtree(self.data_path, ignore_errors=True)
        pass

    def create_document(self, name, content=""):
        with open(os.path.join(self.data_path, name), 'w') as file:
            file.write(content)

if __name__ == "__main__":
    unittest.main()
