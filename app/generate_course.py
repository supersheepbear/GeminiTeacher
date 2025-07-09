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
from pathlib import Path
from typing import Dict, Any, Optional

from cascadellm.coursemaker import create_course, configure_gemini_llm


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
    args = parser.parse_args()
    
    # Get absolute path to config file (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, args.config)
    
    # Load configuration
    config = load_config(config_path)
    
    # Get API key from configuration
    api_key = config.get('api', {}).get('google_api_key')
    if not api_key:
        print("Error: Google API key not found in configuration")
        sys.exit(1)
    
    # Set up environment variables (for backward compatibility)
    setup_environment(config)
    
    # Read input content
    content = read_input_content(args.input)
    
    # Configure the LLM
    model_name = config.get('model', {}).get('name', 'gemini-1.5-pro')
    temperature = config.get('model', {}).get('temperature', 0.0)
    
    if args.verbose:
        print(f"Configuring LLM with model: {model_name} (temperature: {temperature})")
    
    try:
        # Pass the API key directly to avoid authentication issues
        llm = configure_gemini_llm(
            api_key=api_key,
            model_name=model_name, 
            temperature=temperature
        )
        
        # Generate the course with verbose logging
        if args.verbose:
            print(f"Generating course: {args.title}")
            print(f"Maximum chapters: {args.max_chapters}")
            
        course = create_course(
            content, 
            llm=llm, 
            verbose=args.verbose,
            max_chapters=args.max_chapters
        )
        
        # Save the course
        output_dir = config.get('course', {}).get('output_dir', 'output')
        output_dir = os.path.join(script_dir, output_dir)
        
        if args.verbose:
            print(f"Saving course with {len(course.chapters)} chapters to {output_dir}")
            
        save_course_to_files(args.title, course, output_dir)
        
        print(f"Course generated with {len(course.chapters)} chapters")
        print(f"Output saved to: {output_dir}")
        
    except Exception as e:
        print(f"Error generating course: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 