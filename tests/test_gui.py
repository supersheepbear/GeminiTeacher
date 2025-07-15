"""Tests for the GUI module."""
from unittest.mock import patch, MagicMock

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from geminiteacher.gui.main_window import MainWindow, Worker


@pytest.fixture(scope="session")
def app():
    """Create a Qt application instance for testing."""
    # Check if QApplication already exists
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def main_window(app):
    """Create a MainWindow instance for testing."""
    window = MainWindow()
    yield window
    # Clean up
    window.close()


def test_mode_combo_initialization(main_window):
    """Test that the mode combo box is initialized with the correct values."""
    assert main_window.mode_combo.count() == 3
    assert main_window.mode_combo.itemText(0) == "Sequential"
    assert main_window.mode_combo.itemText(1) == "Parallel"
    assert main_window.mode_combo.itemText(2) == "Cascade"


def test_update_ui_for_cascade_mode(main_window):
    """Test that the UI is updated correctly when cascade mode is selected."""
    # Select cascade mode
    main_window.mode_combo.setCurrentIndex(2)
    
    # Check that parallel processing is disabled
    assert main_window.parallel_check.isChecked() is False
    assert main_window.parallel_check.isEnabled() is False
    
    # Check that parallel settings are disabled
    assert main_window.max_workers_spin.isEnabled() is False
    assert main_window.delay_min_spin.isEnabled() is False
    assert main_window.delay_max_spin.isEnabled() is False
    assert main_window.max_retries_spin.isEnabled() is False


def test_update_ui_for_parallel_mode(main_window):
    """Test that the UI is updated correctly when parallel mode is selected."""
    # Select parallel mode
    main_window.mode_combo.setCurrentIndex(1)
    
    # Check that parallel processing is enabled and checked
    assert main_window.parallel_check.isChecked() is True
    assert main_window.parallel_check.isEnabled() is True
    
    # Check that parallel settings are enabled
    assert main_window.max_workers_spin.isEnabled() is True
    assert main_window.delay_min_spin.isEnabled() is True
    assert main_window.delay_max_spin.isEnabled() is True
    assert main_window.max_retries_spin.isEnabled() is True


def test_update_ui_for_sequential_mode(main_window):
    """Test that the UI is updated correctly when sequential mode is selected."""
    # First select cascade mode to disable parallel processing
    main_window.mode_combo.setCurrentIndex(2)
    
    # Then select sequential mode
    main_window.mode_combo.setCurrentIndex(0)
    
    # Check that parallel processing is enabled but not checked
    assert main_window.parallel_check.isEnabled() is True
    
    # Check that parallel settings follow the parallel checkbox state
    parallel_checked = main_window.parallel_check.isChecked()
    assert main_window.max_workers_spin.isEnabled() is parallel_checked
    assert main_window.delay_min_spin.isEnabled() is parallel_checked
    assert main_window.delay_max_spin.isEnabled() is parallel_checked
    assert main_window.max_retries_spin.isEnabled() is parallel_checked


@patch('geminiteacher.gui.main_window.QThread')
@patch('geminiteacher.gui.main_window.Worker')
def test_start_generation_with_cascade_mode(mock_worker_class, mock_thread_class, main_window):
    """Test that the correct parameters are passed to the worker when cascade mode is selected."""
    # Mock the worker and thread
    mock_worker = MagicMock()
    mock_worker_class.return_value = mock_worker
    mock_thread = MagicMock()
    mock_thread_class.return_value = mock_thread
    
    # Set up environment variable to avoid error message
    import os
    os.environ['GOOGLE_API_KEY'] = 'dummy_key'
    
    # Select cascade mode
    main_window.mode_combo.setCurrentIndex(2)
    
    # Set some values in the UI
    main_window.input_file_edit.setText("input.txt")
    main_window.output_dir_edit.setText("output")
    main_window.title_edit.setText("Test Course")
    
    # Trigger the start_generation method
    main_window.start_generation()
    
    # Check that the worker was created with the correct parameters
    mock_worker_class.assert_called_once()
    args, kwargs = mock_worker_class.call_args
    params = args[0]
    
    # Check that the mode parameter is set correctly
    assert params["mode"] == "cascade"
    
    # Check that max_workers is None for cascade mode
    assert params["max_workers"] is None 