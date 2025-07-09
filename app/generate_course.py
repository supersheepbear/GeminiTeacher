#!/usr/bin/env python3
"""
Course Generator App

This script uses the CascadeLLM coursemaker module to generate structured courses
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

from cascadellm.coursemaker import create_course, configure_gemini_llm
from cascadellm.converter import convert_to_markdown


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


def save_course_to_files(course_title: str, course_content: Dict[str, Any], output_dir: str) -> None:
    """
    Save generated course to files.
    
    Parameters
    ----------
    course_title : str
        Title of the course
    course_content : Dict[str, Any]
        Course content dictionary
    output_dir : str
        Directory to save the course files
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Sanitize course title for filename
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in course_title)
    safe_title = safe_title.replace(" ", "_")
    
    # Save course summary
    with open(output_path / f"{safe_title}_summary.md", 'w', encoding='utf-8') as f:
        f.write(f"# {course_title}\n\n")
        f.write(course_content.summary)
    
    # Save each chapter
    for i, chapter in enumerate(course_content.chapters):
        chapter_filename = f"{safe_title}_chapter_{i+1:02d}.md"
        with open(output_path / chapter_filename, 'w', encoding='utf-8') as f:
            f.write(f"# {chapter.title}\n\n")
            f.write("## Summary\n\n")
            f.write(f"{chapter.summary}\n\n")
            f.write("## Explanation\n\n")
            f.write(f"{chapter.explanation}\n\n")
            f.write("## Extension\n\n")
            f.write(f"{chapter.extension}\n")


def main():
    """Main function to run the course generator."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate a structured course from input content")
    parser.add_argument("input", help="Path to the input content file")
    parser.add_argument("--config", default="config.yaml", help="Path to configuration file")
    parser.add_argument("--title", default="Generated Course", help="Title of the course")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--max-chapters", type=int, default=10, help="Maximum number of chapters to generate")
    parser.add_argument("--fixed-chapters", action="store_true", 
                      help="If set, generates exactly --max-chapters chapters instead of adapting based on content complexity")
    parser.add_argument("--custom-prompt", help="Path to a file containing custom instructions for chapter generation")
    parser.add_argument("--log-file", help="Path to log file (default: output/generation_log.txt)")
    args = parser.parse_args()
    
    # Get absolute path to config file (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, args.config)
    
    # Load configuration
    config = load_config(config_path)
    
    # Get output directory
    output_dir = config.get('course', {}).get('output_dir', 'output')
    output_dir = os.path.join(script_dir, output_dir)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up logging
    log_file = args.log_file if args.log_file else os.path.join(output_dir, f"generation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger("generate_course")
    logger.info(f"Starting course generation with config: {config_path}")
    logger.info(f"Input file: {args.input}")
    logger.info(f"Mode: {'Fixed' if args.fixed_chapters else 'Adaptive'} chapter count (max: {args.max_chapters})")
    
    # Read custom prompt if provided
    custom_prompt = None
    if args.custom_prompt:
        try:
            custom_prompt = read_custom_prompt(args.custom_prompt)
            logger.info(f"Using custom prompt from: {args.custom_prompt}")
        except Exception as e:
            logger.error(f"Error reading custom prompt file: {e}", exc_info=True)
            sys.exit(1)
    
    # Get API key from configuration
    api_key = config.get('api', {}).get('google_api_key')
    if not api_key:
        logger.error("Google API key not found in configuration")
        sys.exit(1)
    
    # Set up environment variables (for backward compatibility)
    setup_environment(config)
    
    # Define text-based extensions that do not need conversion
    text_extensions = {".txt", ".md"}
    input_path = Path(args.input)

    # Convert non-text files to Markdown before processing
    if input_path.suffix.lower() not in text_extensions:
        logger.info(f"Input file is not plain text. Converting {args.input} to Markdown...")
        try:
            content = convert_to_markdown(input_path, output_dir=output_dir)
            logger.info(f"Conversion successful. Markdown saved to {output_dir}/{input_path.stem}.md")
        except Exception as e:
            logger.error(f"Error converting file to Markdown: {e}", exc_info=True)
            sys.exit(1)
    else:
        # Read input content directly for text files
        content = read_input_content(args.input)
    
    # Configure the LLM
    model_name = config.get('model', {}).get('name', 'gemini-1.5-pro')
    temperature = config.get('model', {}).get('temperature', 0.0)
    
    logger.info(f"Configuring LLM with model: {model_name} (temperature: {temperature})")
    
    try:
        # Pass the API key directly to avoid authentication issues
        llm = configure_gemini_llm(
            api_key=api_key,
            model_name=model_name, 
            temperature=temperature
        )
        
        # Generate the course with verbose logging
        logger.info(f"Generating course: {args.title}")
        if args.fixed_chapters:
            logger.info(f"Mode: Fixed chapter count (exactly {args.max_chapters} chapters)")
        else:
            logger.info(f"Mode: Adaptive chapter count (1-{args.max_chapters} chapters based on content)")
        
        if custom_prompt:
            logger.info("Using custom prompt for chapter generation")
            
        course = create_course(
            content, 
            llm=llm, 
            verbose=args.verbose,
            max_chapters=args.max_chapters,
            fixed_chapter_count=args.fixed_chapters,
            custom_prompt=custom_prompt
        )
        
        # Save the course
        logger.info(f"Saving course with {len(course.chapters)} chapters to {output_dir}")
            
        save_course_to_files(args.title, course, output_dir)
        
        print(f"Course generated with {len(course.chapters)} chapters")
        print(f"Output saved to: {output_dir}")
        print(f"Log file: {log_file}")
        
    except Exception as e:
        logger.error(f"Error generating course: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main() 