import unittest
from unittest.mock import patch, Mock
from sandbox_scripts.myscript import WikipediaFetcher

class TestWikipediaFetcher(unittest.TestCase):
    @patch('sandbox_scripts.myscript.requests.get')
    def test_fetch_wikipedia_page(self, mock_get):
        # Arrange
        page_title = "Python (programming language)"
        mock_response = Mock()
        
        # Example JSON response
        example_response = {
            "query": {
                "pages": {
                    "12345": {
                        "pageid": 12345,
                        "ns": 0,
                        "title": "Python (programming language)",
                        "extract": "Python is an interpreted, high-level, general-purpose programming language."
                    }
                }
            }
        }
        
        mock_response.json.return_value = example_response
        mock_get.return_value = mock_response
        
        # Act
        result = WikipediaFetcher.fetch_wikipedia_page(page_title)
        
        # Assert
        self.assertEqual(result, "Python is an interpreted, high-level, general-purpose programming language.")
        mock_get.assert_called_once_with(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "prop": "extracts",
                "explaintext": True,
                "titles": page_title,
            }
        )

if __name__ == "__main__":
    unittest.main()