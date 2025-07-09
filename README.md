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

## Setting Up Google Gemini API

This package uses Google's Gemini API for all LLM operations. Follow these steps to set up:

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

## Quick Start

```python
from cascadellm.coursemaker import create_course, configure_gemini_llm

# Load your content
with open("your_content.txt", "r") as f:
    content = f.read()

# Configure Gemini API
llm = configure_gemini_llm()

# Generate a structured course
course = create_course(content, llm=llm)

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
