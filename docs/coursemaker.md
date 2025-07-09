# Course Generator

The `coursemaker` module provides tools for automatically generating structured educational courses from raw content. It's built on LangChain and designed for creating comprehensive learning materials with minimal effort.

## Overview

The course generation process follows a four-phase pipeline:

1. **Table of Contents Generation**: The system analyzes the input content and creates a logical structure with chapter titles.
2. **Prompt Template Creation**: For each chapter, specialized prompts are created to guide the LLM.
3. **Chapter Generation**: Detailed explanations are created for each chapter with a consistent structure.
4. **Summary Generation**: A comprehensive course summary ties everything together.

All generated content is in simplified Chinese and follows a structured format designed for educational purposes.

## Installation

```bash
git clone https://github.com/supersheepbear/CascadeLLM.git
cd CascadeLLM
pip install -e .
```

This package requires the following dependencies:
- langchain >= 0.1.0
- langchain-core >= 0.1.0
- pydantic >= 2.0.0
- langchain-google-genai

## Setting Up Google Gemini API

This module uses Google's Gemini API for all LLM operations:

1. Install the required package:

```bash
pip install langchain-google-genai
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

## Usage

### Basic Usage

Generate a complete course with a single function call:

```python
from cascadellm.coursemaker import create_course, configure_gemini_llm

# Load content from a file or string
with open("your_content.txt", "r") as f:
    raw_content = f.read()

# Configure the Gemini API
llm = configure_gemini_llm()

# Generate a structured course
course = create_course(raw_content, llm=llm)

# The course object contains all generated components
print(f"Generated {len(course.chapters)} chapters")
print(f"Summary: {course.summary[:100]}...")
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

### Using Individual Components

You can also use the individual components of the pipeline:

```python
from cascadellm.coursemaker import generate_toc, generate_chapter, generate_summary, configure_gemini_llm

# Configure the Gemini API
llm = configure_gemini_llm()

# Generate just the table of contents
chapter_titles = generate_toc(raw_content, llm=llm)
print(f"Generated {len(chapter_titles)} chapter titles")

# Generate a single chapter
chapter = generate_chapter("Introduction to AI", raw_content, llm=llm)
print(chapter.title)
print(chapter.summary)

# Generate a summary from chapters
chapters = [chapter]  # You would typically have multiple chapters
summary = generate_summary(raw_content, chapters, llm=llm)
print(summary)
```

### Customizing Gemini Parameters

You can customize the Gemini API parameters:

```python
# Configure with custom parameters
llm = configure_gemini_llm(
    model_name="gemini-1.5-flash",  # Use a different model
    temperature=0.3                  # Adjust temperature for more varied outputs
)

# Use the customized model
course = create_course(raw_content, llm=llm)
```

## API Reference

### Core Functions

::: cascadellm.coursemaker.create_course

::: cascadellm.coursemaker.generate_toc

::: cascadellm.coursemaker.generate_chapter

::: cascadellm.coursemaker.generate_summary

::: cascadellm.coursemaker.configure_gemini_llm

### Data Models

::: cascadellm.coursemaker.Course

::: cascadellm.coursemaker.ChapterContent

### Helper Functions

::: cascadellm.coursemaker.create_toc_prompt

::: cascadellm.coursemaker.create_chapter_prompt_template

::: cascadellm.coursemaker.create_summary_prompt_template

::: cascadellm.coursemaker.parse_chapter_content

## Limitations

- The current implementation is designed for text content only.
- All output is in simplified Chinese.
- For production use, a valid Google API key must be provided.

## Future Enhancements

Future versions may include:
- Support for multiple languages
- Image and multimedia content handling
- Customizable output formats 