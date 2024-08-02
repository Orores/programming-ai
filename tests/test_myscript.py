import unittest
from unittest.mock import patch
import requests
from sandbox_scripts.myscript import WikipediaFetcher

class TestWikipediaFetcher(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_wikipedia_page_success(self, mock_get):
        mock_response = {
            "query": {
                "pages": {
                    "12345": {
                        "pageid": 12345,
                        "ns": 0,
                        "title": "Python (programming language)",
                        "extract": "Python is an interpreted high-level general-purpose programming language."
                    }
                }
            }
        }
        mock_get.return_value.json.return_value = mock_response

        page_title = "Python (programming language)"
        expected_content = "Python is an interpreted high-level general-purpose programming language."
        actual_content = WikipediaFetcher.fetch_wikipedia_page(page_title)
        
        self.assertEqual(expected_content, actual_content)

    @patch('requests.get')
    def test_fetch_wikipedia_page_no_extract(self, mock_get):
        mock_response = {
            "query": {
                "pages": {
                    "12345": {
                        "pageid": 12345,
                        "ns": 0,
                        "title": "Python (programming language)"
                        # No 'extract' field
                    }
                }
            }
        }
        mock_get.return_value.json.return_value = mock_response

        page_title = "Python (programming language)"
        expected_content = ""
        actual_content = WikipediaFetcher.fetch_wikipedia_page(page_title)
        
        self.assertEqual(expected_content, actual_content)

    @patch('requests.get')
    def test_fetch_wikipedia_page_invalid_page(self, mock_get):
        mock_response = {
            "query": {
                "pages": {
                    "-1": {
                        "missing": True
                    }
                }
            }
        }
        mock_get.return_value.json.return_value = mock_response

        page_title = "NonExistentPage"
        expected_content = ""
        actual_content = WikipediaFetcher.fetch_wikipedia_page(page_title)
        
        self.assertEqual(expected_content, actual_content)

    @patch('requests.get')
    def test_fetch_wikipedia_page_error_handling(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")

        page_title = "Python (programming language)"
        with self.assertRaises(requests.exceptions.RequestException):
            WikipediaFetcher.fetch_wikipedia_page(page_title)

    def test_fetch_wikipedia_page_actual_api_call(self):
        page_title = "Python (programming language)"
        content = WikipediaFetcher.fetch_wikipedia_page(page_title)
        
        # Check if the content is not empty
        self.assertNotEqual(content, "")

if __name__ == "__main__":
    unittest.main()
