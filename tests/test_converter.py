"""Tests for the file converter module."""
from unittest.mock import patch, MagicMock

from cascadellm.converter import convert_to_markdown


@patch('cascadellm.converter.MarkItDown')
def test_convert_to_markdown_calls_library_correctly(mock_markitdown_class):
    """
    Tests that the convert_to_markdown wrapper correctly uses the MarkItDown library.
    """
    # Arrange
    # Create a mock instance for the MarkItDown class
    mock_instance = MagicMock()
    # Mock the return value of the convert method
    mock_convert_result = MagicMock()
    mock_convert_result.text_content = "# Mocked Markdown"
    mock_instance.convert.return_value = mock_convert_result

    # Configure the class mock to return our instance mock
    mock_markitdown_class.return_value = mock_instance

    file_path = "dummy/path/to/file.pdf"

    # Act
    result = convert_to_markdown(file_path)

    # Assert
    # Verify that the MarkItDown class was instantiated
    mock_markitdown_class.assert_called_once_with()

    # Verify that the convert method was called on the instance with the correct file path
    mock_instance.convert.assert_called_once_with(file_path)

    # Verify that the function returns the expected text content
    assert result == "# Mocked Markdown" 