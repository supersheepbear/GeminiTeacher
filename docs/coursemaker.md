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

For using Google's Gemini models:
```bash
pip install langchain-google-genai
```

## Setting Up LLM Access

This module is designed to work with any LangChain compatible LLM. The implementation now includes built-in support for Google's Gemini models.

### Using Google's Gemini API

1. Set up your Gemini API key as an environment variable:

```bash
# On Linux/macOS
export GOOGLE_API_KEY=your_gemini_api_key_here

# On Windows PowerShell
$env:GOOGLE_API_KEY = "your_gemini_api_key_here"

# On Windows Command Prompt
set GOOGLE_API_KEY=your_gemini_api_key_here
```

2. Use the built-in helper function to configure Gemini:

```python
from cascadellm.coursemaker import configure_gemini_llm, create_course

# Create a configured Gemini model
llm = configure_gemini_llm(temperature=0.2)  # Optional: provide custom API key with api_key parameter

# Generate a course using the Gemini model
with open("your_content.txt", "r") as f:
    raw_content = f.read()

course = create_course(raw_content, llm=llm)
```

### Using Other LLM Providers

You can use any LangChain compatible LLM by creating an instance and passing it to the functions:

```python
from langchain_openai import ChatOpenAI
from cascadellm.coursemaker import create_course

# Example with OpenAI
llm = ChatOpenAI(
    temperature=0.0,
    model_name="gpt-4-turbo"
)

course = create_course(raw_content, llm=llm)
```

## Usage

### Basic Usage

Generate a complete course with a single function call:

```python
from cascadellm.coursemaker import create_course, configure_gemini_llm

# Load content from a file or string
with open("your_content.txt", "r") as f:
    raw_content = f.read()

# Configure the LLM (optional - if not provided, needs to be mocked in tests)
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

# Configure the LLM
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

## Customization

The module now accepts an LLM parameter in all generation functions, allowing for easy customization:

```python
# Example with a custom LLM configuration
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
import torch

# Create a custom Hugging Face pipeline LLM
pipe = pipeline(
    "text-generation",
    model="bigscience/bloomz-7b1",
    torch_dtype=torch.bfloat16,
    device_map="auto",
    max_new_tokens=512
)

custom_llm = HuggingFacePipeline(pipeline=pipe)

# Use with the course generator
course = create_course(raw_content, llm=custom_llm)
```

## Limitations

- The current implementation is designed for text content only.
- All output is in simplified Chinese.
- For production use, an LLM instance must be provided explicitly.

## Future Enhancements

Future versions may include:
- Support for multiple languages
- Image and multimedia content handling
- Customizable output formats
- Direct integration with additional popular LLM providers 