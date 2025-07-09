# CascadeLLM

[![Release](https://img.shields.io/github/v/release/supersheepbear/CascadeLLM)](https://img.shields.io/github/v/release/supersheepbear/CascadeLLM)
[![Build status](https://img.shields.io/github/actions/workflow/status/supersheepbear/CascadeLLM/main.yml?branch=main)](https://github.com/supersheepbear/CascadeLLM/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/supersheepbear/CascadeLLM/branch/main/graph/badge.svg)](https://codecov.io/gh/supersheepbear/CascadeLLM)
[![Commit activity](https://img.shields.io/github/commit-activity/m/supersheepbear/CascadeLLM)](https://img.shields.io/github/commit-activity/m/supersheepbear/CascadeLLM)
[![License](https://img.shields.io/github/license/supersheepbear/CascadeLLM)](https://img.shields.io/github/license/supersheepbear/CascadeLLM)

**CascadeLLM is my personal toolkit** for building advanced LLM chains and automated workflows. This package is designed for my own use cases and experiments, not as a general-purpose public library. It contains modular components for chaining LLM prompts and transforming content through structured processing pipelines.

> **Note**: This is a personal package not intended for distribution on PyPI. It is shared to showcase LLM chaining techniques and for personal reference.

- **Github repository**: <https://github.com/supersheepbear/CascadeLLM/>
- **Documentation** <https://supersheepbear.github.io/CascadeLLM/>

## Features

### Course Generator

The `coursemaker` module transforms raw content into a structured, educational curriculum with the following steps:

1. **Table of Contents Generation**: Automatically creates chapter titles based on content analysis
2. **Chapter Explanation Generation**: Produces detailed, structured explanations for each chapter
3. **Course Summary**: Creates a comprehensive summary of the entire course

All outputs are in simplified Chinese, with well-structured formatting for each component.

## Installation

Clone the repository and install from source:

```bash
git clone https://github.com/supersheepbear/CascadeLLM.git
cd CascadeLLM
pip install -e .
```

## Setting Up LLM Access

The current implementation uses placeholders for LLM access, which must be configured before use. Here's how to set up Google's Gemini API:

### Using Google's Gemini API

1. Install the Gemini package for LangChain:

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

3. Update the course generator to use Gemini:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from cascadellm.coursemaker import create_course

# Create a wrapper function to use Gemini
def create_course_with_gemini(content, temperature=0.0):
    # Create the Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=temperature
    )
    
    # To use this model, you need to modify the source functions
    # to accept and use this LLM instance instead of the placeholders
    
    # This is a simplified example - a more complete implementation would 
    # modify the internal functions or add parameters to accept the LLM
    
    return create_course(content, temperature=temperature)
```

For a complete implementation, you would need to modify the source code to inject the LLM instance. See the [documentation](https://supersheepbear.github.io/CascadeLLM/coursemaker/) for more details.

## Quick Start

```python
from cascadellm.coursemaker import create_course

# Load your content
with open("your_content.txt", "r") as f:
    content = f.read()

# Generate a structured course
course = create_course(content)

# Access the course components
print(f"Generated {len(course.chapters)} chapters")
print(f"Summary: {course.summary[:100]}...")

# Process individual chapters
for i, chapter in enumerate(course.chapters):
    print(f"Chapter {i+1}: {chapter.title}")
    print(f"Summary: {chapter.summary[:50]}...")
```

## Documentation

For detailed documentation, visit [https://supersheepbear.github.io/CascadeLLM/](https://supersheepbear.github.io/CascadeLLM/)

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
