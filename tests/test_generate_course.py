"""Tests for the generate_course module."""
import os
from unittest.mock import patch, MagicMock

import pytest

from geminiteacher.app.generate_course import create_course_with_progressive_save
from geminiteacher.coursemaker import ChapterContent, Course


@patch('geminiteacher.app.generate_course.parallel_generate_chapters')
@patch('geminiteacher.app.generate_course.generate_chapter')
@patch('geminiteacher.app.generate_course.generate_toc')
@patch('geminiteacher.app.generate_course.configure_gemini_llm')
@patch('geminiteacher.app.generate_course.generate_summary')
@patch('geminiteacher.app.generate_course.save_chapter_to_file')
@patch('builtins.open', new_callable=MagicMock)
def test_create_course_with_progressive_save_sequential_mode(
    mock_open, mock_save_chapter, mock_generate_summary, mock_configure_gemini_llm,
    mock_generate_toc, mock_generate_chapter, mock_parallel_generate_chapters
):
    """Test create_course_with_progressive_save in sequential mode."""
    # Arrange
    mock_llm = MagicMock()
    mock_configure_gemini_llm.return_value = mock_llm
    mock_generate_toc.return_value = ["Chapter 1", "Chapter 2"]
    
    # Create actual ChapterContent objects instead of MagicMocks
    chapter1 = ChapterContent(title="Chapter 1", summary="Summary 1", explanation="Explanation 1", extension="Extension 1")
    chapter2 = ChapterContent(title="Chapter 2", summary="Summary 2", explanation="Explanation 2", extension="Extension 2")
    mock_generate_chapter.side_effect = [chapter1, chapter2]
    
    mock_generate_summary.return_value = "Course summary"
    mock_save_chapter.return_value = "/path/to/chapter.md"
    
    # Act
    result = create_course_with_progressive_save(
        content="Test content",
        course_title="Test Course",
        output_dir="/output",
        max_workers=None  # Sequential mode
    )
    
    # Assert
    assert len(result.chapters) == 2
    assert result.summary == "Course summary"
    assert mock_parallel_generate_chapters.call_count == 0  # Should not be called in sequential mode
    assert mock_generate_chapter.call_count == 2
    assert mock_save_chapter.call_count == 2


@patch('geminiteacher.app.generate_course.parallel_generate_chapters')
@patch('geminiteacher.app.generate_course.generate_chapter')
@patch('geminiteacher.app.generate_course.generate_toc')
@patch('geminiteacher.app.generate_course.configure_gemini_llm')
@patch('geminiteacher.app.generate_course.generate_summary')
@patch('geminiteacher.app.generate_course.save_chapter_to_file')
@patch('builtins.open', new_callable=MagicMock)
def test_create_course_with_progressive_save_parallel_mode(
    mock_open, mock_save_chapter, mock_generate_summary, mock_configure_gemini_llm,
    mock_generate_toc, mock_generate_chapter, mock_parallel_generate_chapters
):
    """Test create_course_with_progressive_save in parallel mode."""
    # Arrange
    mock_llm = MagicMock()
    mock_configure_gemini_llm.return_value = mock_llm
    mock_generate_toc.return_value = ["Chapter 1", "Chapter 2"]
    
    # Create actual ChapterContent objects instead of MagicMocks
    chapter1 = ChapterContent(title="Chapter 1", summary="Summary 1", explanation="Explanation 1", extension="Extension 1")
    chapter2 = ChapterContent(title="Chapter 2", summary="Summary 2", explanation="Explanation 2", extension="Extension 2")
    mock_parallel_generate_chapters.return_value = [chapter1, chapter2]
    
    mock_generate_summary.return_value = "Course summary"
    
    # Act
    result = create_course_with_progressive_save(
        content="Test content",
        course_title="Test Course",
        output_dir="/output",
        max_workers=2,  # Parallel mode
        mode="parallel"
    )
    
    # Assert
    assert len(result.chapters) == 2
    assert result.summary == "Course summary"
    assert mock_parallel_generate_chapters.call_count == 1
    assert mock_generate_chapter.call_count == 0  # Should not be called in parallel mode


@patch('geminiteacher.app.generate_course.create_course_cascade')
@patch('geminiteacher.app.generate_course.generate_toc')
@patch('geminiteacher.app.generate_course.configure_gemini_llm')
@patch('geminiteacher.app.generate_course.generate_summary')
@patch('geminiteacher.app.generate_course.save_chapter_to_file')
@patch('builtins.open', new_callable=MagicMock)
def test_create_course_with_progressive_save_cascade_mode(
    mock_open, mock_save_chapter, mock_generate_summary, mock_configure_gemini_llm,
    mock_generate_toc, mock_create_course_cascade
):
    """Test create_course_with_progressive_save in cascade mode."""
    # Arrange
    mock_llm = MagicMock()
    mock_configure_gemini_llm.return_value = mock_llm
    
    # Create actual ChapterContent objects
    chapter1 = ChapterContent(title="Chapter 1", summary="Summary 1", explanation="Explanation 1", extension="Extension 1")
    chapter2 = ChapterContent(title="Chapter 2", summary="Summary 2", explanation="Explanation 2", extension="Extension 2")
    
    # Create an actual Course object
    mock_course = Course(
        chapters=[chapter1, chapter2],
        summary="Course summary",
        content="Test content"
    )
    mock_create_course_cascade.return_value = mock_course
    
    # Act
    result = create_course_with_progressive_save(
        content="Test content",
        course_title="Test Course",
        output_dir="/output",
        mode="cascade"
    )
    
    # Assert
    assert len(result.chapters) == 2
    assert result.summary == "Course summary"
    assert mock_create_course_cascade.call_count == 1
    
    # Update the assertion to match the actual function call
    mock_create_course_cascade.assert_called_once_with(
        content="Test content",
        llm=mock_llm,
        temperature=0.0,
        verbose=False,
        max_chapters=10,
        fixed_chapter_count=False,
        custom_prompt=None
    ) 