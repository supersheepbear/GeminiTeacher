# GeminiTeacher

[![PyPI version](https://badge.fury.io/py/geminiteacher.svg)](https://badge.fury.io/py/geminiteacher)
[![Build status](https://img.shields.io/github/actions/workflow/status/supersheepbear/GeminiTeacher/main.yml?branch=main)](https://github.com/supersheepbear/GeminiTeacher/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/supersheepbear/GeminiTeacher/branch/main/graph/badge.svg)](https://codecov.io/gh/supersheepbear/GeminiTeacher)
[![License](https://img.shields.io/github/license/supersheepbear/GeminiTeacher)](https://img.shields.io/github/license/supersheepbear/GeminiTeacher)

**GeminiTeacher** is an AI-powered course creation toolkit using Google's Gemini LLM. It transforms raw text, markdown, or documents into structured, lesson-based educational content. Ideal for educators, developers, and content creators.

- **Full Documentation**: [https://supersheepbear.github.io/GeminiTeacher/](https://supersheepbear.github.io/GeminiTeacher/)
- **Source Code**: [https://github.com/supersheepbear/GeminiTeacher/](https://github.com/supersheepbear/GeminiTeacher/)

## Quick Start

The best way to use GeminiTeacher is with the command-line interface and a `config.yaml` file.

### 1. Installation

First, install the package and set up your API key by following the [**Installation and Setup Guide**](./docs/installation.md).

### 2. Create Your Content

Create a text file with the raw material for your course. For example, `my_notes.txt`.

```text
// my_notes.txt
Machine learning is a subfield of artificial intelligence that focuses on developing 
systems that can learn from and make decisions based on data. Unlike traditional 
programming where explicit instructions are provided, machine learning algorithms 
build models based on sample data to make predictions or decisions without being 
explicitly programmed to do so. Supervised learning involves labeled data, while
unsupervised learning deals with unlabeled data. Reinforcement learning is about
agents taking actions in an environment to maximize cumulative reward.
```

### 3. Create a Configuration File

Next, create a `config.yaml` to define how you want your course to be generated.

```yaml
# config.yaml
input:
  path: "my_notes.txt"
output:
  directory: "output/machine_learning_course"
course:
  title: "Introduction to Machine Learning"
generation:
  max_chapters: 5
  fixed_chapter_count: true
parallel:
  enabled: true
```

### 4. Run the Generator

Now, run the command from your terminal:

```bash
geminiteacher --config config.yaml
```

The tool will create the specified output directory and fill it with structured markdown files for each chapter and a course summary.

## Key Features

- **Automated Course Structuring**: Intelligently organizes raw text into logical, lesson-based chapters.
- **Config-Driven Workflow**: Use a simple YAML file to control all aspects of course generation.
- **Parallel Processing**: Generates chapters concurrently to dramatically reduce creation time.
- **CLI & Python API**: Use the powerful command-line tool for no-code generation or the Python API for programmatic control.
- **Customizable AI Behavior**: Use custom prompts and temperature controls to tailor the output to your needs.
- **Robust and Reliable**: Includes progressive saving and automatic retries for network errors.

## Learn More

For more advanced CLI options, programmatic Python API usage, and troubleshooting, please see the full [**Usage Guide**](./docs/usage.md).

## Contributing

Contributions are welcome! Please check out our [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
