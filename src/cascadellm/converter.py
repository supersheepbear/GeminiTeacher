"""This module handles file conversions to Markdown."""
from pathlib import Path
from markitdown import MarkItDown


def convert_to_markdown(file_path: str | Path) -> str:
    """
    Converts a given file to Markdown using the markitdown library.

    This function acts as a wrapper around the MarkItDown library,
    handling initialization and conversion for various file types
    supported by the library.

    Parameters
    ----------
    file_path : str or Path
        The path to the file to be converted.

    Returns
    -------
    str
        The Markdown content of the file.
    """
    md = MarkItDown()
    result = md.convert(str(file_path))
    return result.text_content 