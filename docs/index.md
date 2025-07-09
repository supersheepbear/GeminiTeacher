# CascadeLLM

[![Release](https://img.shields.io/github/v/release/supersheepbear/CascadeLLM)](https://img.shields.io/github/v/release/supersheepbear/CascadeLLM)
[![Build status](https://img.shields.io/github/actions/workflow/status/supersheepbear/CascadeLLM/main.yml?branch=main)](https://github.com/supersheepbear/CascadeLLM/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/supersheepbear/CascadeLLM)](https://img.shields.io/github/commit-activity/m/supersheepbear/CascadeLLM)
[![License](https://img.shields.io/github/license/supersheepbear/CascadeLLM)](https://img.shields.io/github/license/supersheepbear/CascadeLLM)

CascadeLLM is a toolkit for building advanced LLM chains and automated workflows. It contains modular components for chaining LLM prompts and transforming content through structured processing pipelines.

## Available Modules

### Course Generator

The `coursemaker` module transforms raw content into a structured, educational curriculum with the following steps:

1. **Table of Contents Generation**: Automatically creates chapter titles based on content analysis
2. **Chapter Explanation Generation**: Produces detailed, structured explanations for each chapter
3. **Course Summary**: Creates a comprehensive summary of the entire course

All outputs are in simplified Chinese, with well-structured formatting for each component.

```python
from cascadellm.coursemaker import create_course

# Generate a structured course from raw content
course = create_course("Your raw content here")

# Access the generated course components
print(f"Generated {len(course.chapters)} chapters")
for chapter in course.chapters:
    print(f"- {chapter.title}")
```

[Learn more about the Course Generator](./coursemaker.md)

## Installation

Clone the repository and install from source:

```bash
git clone https://github.com/supersheepbear/CascadeLLM.git
cd CascadeLLM
pip install -e .
```

## Requirements

- Python 3.9+
- langchain >= 0.1.0
- langchain-core >= 0.1.0
- pydantic >= 2.0.0

## Contributing

Contributions are welcome! This repository is designed to be a collection of modular components for building LLM-powered applications. If you have ideas for new modules or improvements to existing ones, feel free to contribute.
