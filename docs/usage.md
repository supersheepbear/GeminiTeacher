# Usage Guide

GeminiTeacher provides powerful tools for automatically generating structured educational courses from raw text content. This guide will walk you through the installation, setup, and various ways to use the package.

## Overview

The course generation process follows a four-phase pipeline:

1. **Table of Contents Generation**: The system analyzes the input content and creates a logical structure with chapter titles.
2. **Chapter Generation**: Detailed explanations are created for each chapter with a consistent structure.
3. **Summary Generation**: A comprehensive course summary ties everything together.
4. **File Saving**: When using parallel processing, chapters are saved to disk as they're generated.

All generated content follows a structured format designed for educational purposes.

## Installation

Install GeminiTeacher directly from PyPI:

```bash
pip install geminiteacher
```

## Setting Up Google Gemini API

GeminiTeacher uses Google's Gemini API for all LLM operations:

1. Make sure you have the package installed:

```bash
pip install geminiteacher
```

2. Set up your Gemini API key as an environment variable:

```bash
# On Linux/macOS
export GOOGLE_API_KEY=your_gemini_api_key_here

# On Windows PowerShell
$env:GOOGLE_API_KEY = "your_gemini_api_key_here"

# On Windows Command Prompt
set GOOGLE_API_KEY=your_gemini_api_key_here
```

## Command-line Usage

The easiest way to use GeminiTeacher is through its command-line interface, which is automatically installed with the package.

### Basic Command-line Usage

After installation, you can use the `geminiteacher` command directly:

```bash
# Generate a course from a text file
geminiteacher --input content.txt --output-dir courses --title "Machine Learning Basics"

# If the command is not found, you can use the Python module syntax:
python -m geminiteacher.app.generate_course --input content.txt --output-dir courses
```

### Advanced Command-line Options

For more control, you can use additional command-line options:

```bash
# Enable parallel processing for faster generation
geminiteacher --input content.txt --parallel --max-workers 4

# Set a specific temperature for more creative outputs
geminiteacher --input content.txt --temperature 0.3

# Use a custom prompt file for specialized instructions
geminiteacher --input content.txt --custom-prompt my_instructions.txt

# Generate a fixed number of chapters
geminiteacher --input content.txt --max-chapters 5 --fixed-chapter-count
```

### Using a Configuration File

For the most control, create a `config.yaml` file:

```yaml
# API Configuration
api:
  google_api_key: "your_gemini_api_key_here"  # Or use environment variable
  model_name: "gemini-1.5-pro"

# Input/Output Settings
input:
  path: "input/content.txt"

output:
  directory: "output"

# Course Settings
course:
  title: "Machine Learning"
  custom_prompt: "custom_instructions.txt"

# Generation Settings
generation:
  temperature: 0.2
  max_chapters: 10
  fixed_chapter_count: false

# Parallel Processing Settings
parallel:
  enabled: true
  max_workers: 4
  delay_min: 0.2
  delay_max: 0.8
  max_retries: 3
```

Then run:

```bash
geminiteacher --config config.yaml
```

For complete details on the command-line interface, see the [CLI Application](app.md) documentation.

## Python API Usage

### Quick Start

If you prefer to use GeminiTeacher programmatically, you can use the high-level import:

```python
import geminiteacher as gt

# Load content from a file or string
with open("your_content.txt", "r") as f:
    raw_content = f.read()

# Generate a structured course
course = gt.create_course(raw_content)

# The course object contains all generated components
print(f"Generated {len(course.chapters)} chapters")
print(f"Summary: {course.summary[:100]}...")
```

### Parallel Processing for Speed

For faster course generation, use parallel processing to generate chapters concurrently:

```python
import geminiteacher as gt

# Load content from a file or string
with open("your_content.txt", "r") as f:
    raw_content = f.read()

# Generate a structured course with parallel processing
course = gt.create_course_parallel(
    raw_content, 
    max_workers=4,              # Number of parallel workers
    delay_range=(0.2, 0.8),     # Random delay between API requests
    max_retries=3,              # Retry attempts for failed API calls
    course_title="my_course",   # Title for saved files
    output_dir="courses"        # Directory to save generated chapters
)

# The course object contains all generated components
print(f"Generated {len(course.chapters)} chapters in parallel")
print(f"Summary: {course.summary[:100]}...")
```

### Using the App Module Directly

For more advanced features like progressive saving and detailed logging:

```python
from geminiteacher.app import create_course_with_progressive_save, configure_logging

# Configure logging
logger = configure_logging(log_file="generation.log", verbose=True)

# Generate a course with progressive saving
course = create_course_with_progressive_save(
    content="Your content here...",
    course_title="Python Programming",
    output_dir="courses",
    temperature=0.2,
    max_chapters=5,
    custom_prompt="Focus on practical examples",
    verbose=True,
    logger=logger
)
```

### Accessing Course Components

The course generator produces structured data that you can easily access:

```python
# Iterate through chapters
for i, chapter in enumerate(course.chapters):
    print(f"Chapter {i+1}: {chapter.title}")
    print("Summary:", chapter.summary)
    print("Explanation:", chapter.explanation[:100] + "...")
    print("Extension:", chapter.extension[:100] + "...")
    print("---")

# Access the course summary
print("Course Summary:", course.summary)
```

## Advanced Usage

### Using Individual Components

You can also use the individual components of the pipeline for more control:

```python
from geminiteacher import configure_gemini_llm, generate_toc, generate_chapter, generate_summary

# Configure the Gemini API with custom parameters
llm = configure_gemini_llm(
    model_name="gemini-1.5-flash",  # Use a different model
    temperature=0.3                  # Adjust temperature for more varied outputs
)

# Generate just the table of contents
chapter_titles = generate_toc(
    raw_content, 
    llm=llm,
    max_chapters=5,            # Maximum number of chapters
    fixed_chapter_count=True   # Generate exactly 5 chapters
)
print(f"Generated {len(chapter_titles)} chapter titles")

# Generate a single chapter
chapter = generate_chapter(
    "Introduction to AI", 
    raw_content, 
    llm=llm,
    custom_prompt="Focus on practical examples and code snippets."
)
print(chapter.title)
print(chapter.summary)

# Generate a summary from chapters
chapters = [chapter]  # You would typically have multiple chapters
summary = generate_summary(raw_content, chapters, llm=llm)
print(summary)
```

### Using Parallel Components

For more control over the parallel processing:

```python
from geminiteacher import generate_toc, generate_summary, configure_gemini_llm
from geminiteacher.parallel import parallel_generate_chapters

# Configure the Gemini API
llm = configure_gemini_llm()

# Generate table of contents
chapter_titles = generate_toc(raw_content, llm=llm)

# Generate chapters in parallel with custom parameters
chapters = parallel_generate_chapters(
    chapter_titles=chapter_titles,
    content=raw_content,
    llm=llm,
    max_workers=4,
    delay_range=(0.2, 0.8),
    max_retries=3,
    course_title="advanced_course",
    output_dir="output/courses"
)

# Generate a summary from the chapters
summary = generate_summary(raw_content, chapters, llm=llm)
```

### Custom Prompts

You can customize how chapters are generated by providing custom instructions:

```python
import geminiteacher as gt

custom_prompt = """
Focus on practical examples and include code snippets where relevant.
Each concept should be explained with a real-world application.
Include exercises at the end of each explanation section.
"""

course = gt.create_course(
    raw_content,
    custom_prompt=custom_prompt,
    temperature=0.3  # Higher temperature for more creative outputs
)
```

## API Reference

### Core Functions

::: geminiteacher.coursemaker.create_course

::: geminiteacher.coursemaker.create_course_parallel

::: geminiteacher.coursemaker.generate_toc

::: geminiteacher.coursemaker.generate_chapter

::: geminiteacher.coursemaker.generate_summary

::: geminiteacher.coursemaker.configure_gemini_llm

### Parallel Processing

::: geminiteacher.parallel.parallel_generate_chapters

::: geminiteacher.parallel.generate_chapter_with_retry

::: geminiteacher.parallel.parallel_map_with_delay

### App Module

::: geminiteacher.app.generate_course.create_course_with_progressive_save

::: geminiteacher.app.generate_course.configure_logging

### Data Models

::: geminiteacher.coursemaker.Course

::: geminiteacher.coursemaker.ChapterContent

## Limitations

- For production use, a valid Google API key must be provided.
- API rate limits may affect parallel processing performance.
- Large content may require higher token limits from your Gemini API plan. 