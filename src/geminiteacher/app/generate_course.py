#!/usr/bin/env python3
"""
Course Generator App

This script uses the GeminiTeacher coursemaker module to generate structured courses
from input content, using configuration from a YAML file.
"""

import argparse
import os
import sys
import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from geminiteacher import create_course, configure_gemini_llm, Course
from geminiteacher.parallel import parallel_generate_chapters


def configure_logging(log_file=None, verbose=False):
    """
    Configure logging for the application.
    
    Parameters
    ----------
    log_file : str, optional
        Path to the log file
    verbose : bool, optional
        Whether to use verbose (DEBUG) logging
    
    Returns
    -------
    logging.Logger
        Configured logger instance
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # Console handler
        ]
    )
    
    # Create a logger for this application
    logger = logging.getLogger("geminiteacher.app")
    
    # Add file handler if log_file is provided
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(log_level)
        
        # Add the file handler to the logger
        logger.addHandler(file_handler)
        
        # Also add the file handler to the geminiteacher loggers
        for module in ["geminiteacher", "geminiteacher.coursemaker", "geminiteacher.parallel"]:
            module_logger = logging.getLogger(module)
            module_logger.addHandler(file_handler)
            module_logger.setLevel(log_level)
    
    # Set environment variable with log level for worker processes
    os.environ["GeminiTeacher_LOG_LEVEL"] = str(log_level)
    
    return logger


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Parameters
    ----------
    config_path : str
        Path to the YAML configuration file
        
    Returns
    -------
    Dict[str, Any]
        Configuration dictionary
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)


def setup_environment(config: Dict[str, Any]) -> None:
    """
    Set up environment variables from configuration.
    
    Parameters
    ----------
    config : Dict[str, Any]
        Configuration dictionary
    """
    # Set Google API key as environment variable
    if 'api' in config and 'google_api_key' in config['api']:
        os.environ['GOOGLE_API_KEY'] = config['api']['google_api_key']
    else:
        print("Warning: Google API key not found in configuration")


def read_input_content(input_path: str) -> str:
    """
    Read content from an input file.
    
    Parameters
    ----------
    input_path : str
        Path to the input file
        
    Returns
    -------
    str
        Content of the input file
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)


def read_custom_prompt(file_path: str) -> str:
    """
    Read custom prompt instructions from a file.
    
    Parameters
    ----------
    file_path : str
        Path to the file containing custom prompt instructions
        
    Returns
    -------
    str
        Content of the custom prompt file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            custom_prompt = f.read().strip()
        return custom_prompt
    except Exception as e:
        print(f"Error reading custom prompt file: {e}")
        sys.exit(1)


def save_chapter_to_file(course_title: str, chapter: Any, chapter_index: int, output_dir: str) -> str:
    """
    Save a single chapter to a file.
    
    Parameters
    ----------
    course_title : str
        Title of the course
    chapter : Any
        Chapter content object
    chapter_index : int
        Index of the chapter (0-based)
    output_dir : str
        Directory to save the chapter file
        
    Returns
    -------
    str
        Path to the saved chapter file
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Sanitize course title for filename
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in course_title)
    safe_title = safe_title.replace(" ", "_")
    
    # Create chapter filename with chapter number and title
    chapter_title_safe = "".join(c if c.isalnum() or c in " -_" else "_" for c in chapter.title)
    chapter_title_safe = chapter_title_safe.replace(" ", "_")
    chapter_filename = f"{safe_title}_chapter_{chapter_index+1:02d}_{chapter_title_safe}.md"
    chapter_path = output_path / chapter_filename
    
    # Save chapter content
    with open(chapter_path, 'w', encoding='utf-8') as f:
        f.write(f"# {chapter.title}\n\n")
        f.write("## Summary\n\n")
        f.write(f"{chapter.summary}\n\n")
        f.write("## Explanation\n\n")
        f.write(f"{chapter.explanation}\n\n")
        f.write("## Extension\n\n")
        f.write(f"{chapter.extension}\n")
    
    return str(chapter_path)


def save_course_to_files(course_title: str, course_content: Course, output_dir: str) -> None:
    """
    Save course content to files.
    
    Parameters
    ----------
    course_title : str
        Title of the course
    course_content : Course
        Course content object
    output_dir : str
        Directory to save the course files
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Sanitize course title for filename
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in course_title)
    safe_title = safe_title.replace(" ", "_")
    
    # Save each chapter to a separate file
    for i, chapter in enumerate(course_content.chapters):
        save_chapter_to_file(safe_title, chapter, i, output_dir)
    
    # Save course summary
    summary_filename = f"{safe_title}_summary.md"
    summary_path = output_path / summary_filename
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"# {course_title} - Course Summary\n\n")
        f.write(f"{course_content.summary}\n\n")
        f.write("## Chapters\n\n")
        
        for i, chapter in enumerate(course_content.chapters):
            f.write(f"{i+1}. {chapter.title}\n")


def create_course_with_progressive_save(
    content: str,
    course_title: str,
    output_dir: str,
    llm=None,
    temperature: float = 0.0,
    verbose: bool = False,
    max_chapters: int = 10,
    fixed_chapter_count: bool = False,
    custom_prompt: Optional[str] = None,
    max_workers: Optional[int] = None,
    delay_range: tuple = (0.1, 0.5),
    max_retries: int = 3,
    logger=None
) -> Course:
    """
    Generate a course with progressive saving of chapters.
    
    This function creates a course and saves each chapter as it's generated,
    providing a more robust approach for long-running generations.
    
    Parameters
    ----------
    content : str
        The raw content to transform into a course
    course_title : str
        Title of the course
    output_dir : str
        Directory to save the generated files
    llm : Optional[BaseLanguageModel], optional
        Language model to use. If None, a default model will be configured.
    temperature : float, optional
        Temperature for generation. Default is 0.0.
    verbose : bool, optional
        Whether to print progress messages. Default is False.
    max_chapters : int, optional
        Maximum number of chapters. Default is 10.
    fixed_chapter_count : bool, optional
        Whether to use fixed chapter count. Default is False.
    custom_prompt : Optional[str], optional
        Custom prompt instructions. Default is None.
    max_workers : Optional[int], optional
        Maximum number of worker processes. If None, uses the default.
    delay_range : tuple, optional
        Range (min, max) in seconds for the random delay between task submissions.
        Default is (0.1, 0.5).
    max_retries : int, optional
        Maximum number of retry attempts per chapter. Default is 3.
    logger : Optional[logging.Logger], optional
        Logger instance to use. If None, a new logger will be created.
        
    Returns
    -------
    Course
        The generated course object
    """
    if logger is None:
        logger = logging.getLogger("geminiteacher.app")
    
    # Create the course using parallel processing with progressive saving
    course = create_course(
        content,
        llm=llm,
        temperature=temperature,
        verbose=verbose,
        max_chapters=max_chapters,
        fixed_chapter_count=fixed_chapter_count,
        custom_prompt=custom_prompt
    )
    
    # Save the course to files
    save_course_to_files(course_title, course, output_dir)
    
    return course


def main():
    """
    Main entry point for the course generator application.
    """
    parser = argparse.ArgumentParser(description="Generate a structured course from input content.")
    parser.add_argument("--config", "-c", type=str, default="config.yaml", help="Path to configuration file")
    parser.add_argument("--input", "-i", type=str, help="Path to input content file")
    parser.add_argument("--output-dir", "-o", type=str, default="output", help="Directory to save generated course files")
    parser.add_argument("--title", "-t", type=str, help="Course title")
    parser.add_argument("--custom-prompt", "-p", type=str, help="Path to custom prompt instructions file")
    parser.add_argument("--temperature", type=float, help="Temperature for generation (0.0-1.0)")
    parser.add_argument("--max-chapters", type=int, help="Maximum number of chapters")
    parser.add_argument("--fixed-chapter-count", action="store_true", help="Generate exactly max-chapters chapters")
    parser.add_argument("--parallel", action="store_true", help="Use parallel processing for chapter generation")
    parser.add_argument("--max-workers", type=int, help="Maximum number of worker processes for parallel generation")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--log-file", type=str, help="Path to log file")
    
    args = parser.parse_args()
    
    # Configure logging
    logger = configure_logging(args.log_file, args.verbose)
    
    # Load configuration
    config = load_config(args.config)
    
    # Set up environment variables
    setup_environment(config)
    
    # Get parameters from command-line arguments or configuration
    input_path = args.input or config.get('input', {}).get('path')
    if not input_path:
        logger.error("Input file path not specified")
        sys.exit(1)
    
    output_dir = args.output_dir or config.get('output', {}).get('directory', 'output')
    course_title = args.title or config.get('course', {}).get('title', 'Untitled Course')
    
    # Read custom prompt if specified
    custom_prompt = None
    if args.custom_prompt:
        custom_prompt = read_custom_prompt(args.custom_prompt)
    elif 'custom_prompt' in config.get('course', {}):
        custom_prompt_path = config['course']['custom_prompt']
        if custom_prompt_path:
            custom_prompt = read_custom_prompt(custom_prompt_path)
    
    # Get generation parameters
    temperature = args.temperature if args.temperature is not None else config.get('generation', {}).get('temperature', 0.0)
    max_chapters = args.max_chapters or config.get('generation', {}).get('max_chapters', 10)
    fixed_chapter_count = args.fixed_chapter_count or config.get('generation', {}).get('fixed_chapter_count', False)
    
    # Parallel processing parameters
    use_parallel = args.parallel or config.get('parallel', {}).get('enabled', False)
    max_workers = args.max_workers or config.get('parallel', {}).get('max_workers')
    delay_min = config.get('parallel', {}).get('delay_min', 0.1)
    delay_max = config.get('parallel', {}).get('delay_max', 0.5)
    delay_range = (delay_min, delay_max)
    max_retries = config.get('parallel', {}).get('max_retries', 3)
    
    # Read input content
    logger.info(f"Reading input content from {input_path}")
    content = read_input_content(input_path)
    
    # Configure the LLM
    logger.info("Configuring language model")
    llm = configure_gemini_llm(
        model_name=config.get('api', {}).get('model_name', "gemini-1.5-pro"),
        temperature=temperature
    )
    
    # Generate the course
    logger.info(f"Generating course with title: {course_title}")
    logger.info(f"Using temperature: {temperature}")
    logger.info(f"Maximum chapters: {max_chapters}")
    logger.info(f"Fixed chapter count: {fixed_chapter_count}")
    logger.info(f"Custom prompt: {'Yes' if custom_prompt else 'No'}")
    
    start_time = datetime.now()
    
    if use_parallel:
        logger.info("Using parallel processing for chapter generation")
        logger.info(f"Max workers: {max_workers or 'Default'}")
        logger.info(f"Delay range: {delay_range}")
        logger.info(f"Max retries: {max_retries}")
        
        course = create_course_with_progressive_save(
            content=content,
            course_title=course_title,
            output_dir=output_dir,
            llm=llm,
            temperature=temperature,
            verbose=args.verbose,
            max_chapters=max_chapters,
            fixed_chapter_count=fixed_chapter_count,
            custom_prompt=custom_prompt,
            max_workers=max_workers,
            delay_range=delay_range,
            max_retries=max_retries,
            logger=logger
        )
    else:
        logger.info("Using sequential processing for chapter generation")
        
        course = create_course_with_progressive_save(
            content=content,
            course_title=course_title,
            output_dir=output_dir,
            llm=llm,
            temperature=temperature,
            verbose=args.verbose,
            max_chapters=max_chapters,
            fixed_chapter_count=fixed_chapter_count,
            custom_prompt=custom_prompt,
            logger=logger
        )
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    # Print summary
    logger.info(f"Course generation completed in {duration}")
    logger.info(f"Generated {len(course.chapters)} chapters")
    logger.info(f"Output saved to {output_dir}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 