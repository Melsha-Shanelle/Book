import pytest
from unittest.mock import patch
import home  

@patch('NewHome.requests.post')  # This mocks the requests.post call in NewHome.py
def test_filter_books_success(mock_post):
    # Set up the mock to return a successful response when called
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = [{"title": "Test Book", "author": "Test Author"}]

    # Call the function under test
    books = NewHome.filter_books("happy", 25, "New York")

    # Assertions to check if filter_books behaves as expected
    assert len(books) == 1, "Expected one book in the result"
    assert books[0]["title"] == "Test Book", "Book title does not match expected"
    assert books[0]["author"] == "Test Author", "Author name does not match expected"

@patch('NewHome.requests.post')  # Mock the requests.post call for failure scenario
def test_filter_books_failure(mock_post):
    # Set up the mock to simulate an API failure
    mock_response = mock_post.return_value
    mock_response.status_code = 500  # Simulate server error

    # Call the function under test
    books = NewHome.filter_books("happy", 25, "New York")

    # Assertions to check correct handling of the failure
    assert books == [], "Expected no books on API failure"
    

