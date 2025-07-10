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

This repository contains various tools and modules for personal LLM projects.

### Course Generator

A key feature is the `coursemaker` module, which automatically transforms raw text content into a structured educational course. An example application demonstrating this functionality can be found in the `app` directory. See the `app/README.md` for instructions on how to run it.

Key capabilities of the Course Generator include:

- **Multi-format Input**: Process various document formats (PDF, DOCX, PPTX, etc.) by automatically converting them to Markdown
- **Adaptive Chapter Generation**: AI determines the optimal number of chapters based on content complexity
- **Fixed Chapter Count Mode**: Generate exactly the specified number of chapters when needed
- **Custom Prompt Instructions**: Customize how the AI generates chapter explanations by providing additional instructions
- **Structured Output**: Generate well-organized course materials with summaries, detailed explanations, and extension thoughts
- **Parallel Processing**: Generate chapters concurrently for significantly faster course creation
- **Robust Error Handling**: Automatically retry failed API calls with exponential backoff

### Parallel Processing

The `parallel` module provides utilities for efficient parallel execution with API rate limiting:

- **Controlled Concurrency**: Configure the number of parallel workers to match your system resources
- **Rate Limit Management**: Add randomized delays between API requests to avoid hitting rate limits
- **Robust Error Handling**: Automatically retry failed requests with exponential backoff
- **Ordered Results**: Ensure outputs are returned in the same order as inputs, regardless of completion time

## Installation

This project is set up as a Python package. To install it for development, clone the repository and use `pip`:

```bash
git clone https://github.com/supersheepbear/CascadeLLM.git
cd CascadeLLM
pip install -e .
```

## Documentation

For detailed documentation, visit [https://supersheepbear.github.io/CascadeLLM/](https://supersheepbear.github.io/CascadeLLM/)

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
