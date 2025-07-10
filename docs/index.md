# GeminiTeacher

[![PyPI version](https://badge.fury.io/py/geminiteacher.svg)](https://badge.fury.io/py/geminiteacher)
[![Build status](https://img.shields.io/github/actions/workflow/status/supersheepbear/GeminiTeacher/main.yml?branch=main)](https://github.com/supersheepbear/GeminiTeacher/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/supersheepbear/GeminiTeacher/branch/main/graph/badge.svg)](https://codecov.io/gh/supersheepbear/GeminiTeacher)
[![License](https://img.shields.io/github/license/supersheepbear/GeminiTeacher)](https://img.shields.io/github/license/supersheepbear/GeminiTeacher)

**GeminiTeacher** is an educational content generation toolkit powered by Google's Gemini LLM. It transforms raw text content into structured, well-organized educational courses with minimal effort. Perfect for educators, content creators, and anyone looking to quickly create high-quality learning materials.

## Installation

Install GeminiTeacher directly from PyPI:

```bash
pip install geminiteacher
```

You'll need a Google API key with access to Gemini models. Set it as an environment variable:

```bash
# For Linux/macOS
export GOOGLE_API_KEY="your-api-key-here"

# For Windows (Command Prompt)
set GOOGLE_API_KEY=your-api-key-here

# For Windows (PowerShell)
$env:GOOGLE_API_KEY="your-api-key-here"
```

## Command-line Usage

After installation, you can immediately use the `geminiteacher` command-line tool without writing any code:

```bash
# Basic usage with a text file
geminiteacher --input content.txt --output-dir courses --title "Machine Learning Basics"

# Enable parallel processing for faster generation
geminiteacher --input content.txt --parallel --max-workers 4

# Use a configuration file for more control
geminiteacher --config config.yaml
```

For detailed command-line options and examples, see the [CLI Application](app.md) documentation.

## Python API Usage

Generate a complete course with just a few lines of code:

```python
import geminiteacher as gt

# Your raw content to transform into a course
content = """
Machine learning is a subfield of artificial intelligence that focuses on developing 
systems that can learn from and make decisions based on data. Unlike traditional 
programming where explicit instructions are provided, machine learning algorithms 
build models based on sample data to make predictions or decisions without being 
explicitly programmed to do so.
"""

# Generate a course with parallel processing for speed
course = gt.create_course_parallel(
    content=content,
    max_chapters=5,          # Maximum number of chapters to generate
    fixed_chapter_count=True,  # Generate exactly 5 chapters
    temperature=0.2,         # Control creativity (0.0-1.0)
    verbose=True             # Show progress messages
)

# Print the generated course structure
print(f"Course Summary: {course.summary}\n")
print(f"Generated {len(course.chapters)} chapters:")
for i, chapter in enumerate(course.chapters):
    print(f"  {i+1}. {chapter.title}")
```

## Documentation

For detailed usage instructions and API documentation, check out the following sections:

- [Usage Guide](usage.md) - Detailed guide on using the course generator
- [CLI Application](app.md) - Command-line interface documentation
- [Modules Overview](modules.md) - Overview of the package structure
- [Parallel Processing](parallel.md) - Advanced parallel processing features
