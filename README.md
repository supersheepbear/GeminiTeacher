# GeminiTeacher

[![PyPI version](https://badge.fury.io/py/geminiteacher.svg)](https://badge.fury.io/py/geminiteacher)
[![Build status](https://img.shields.io/github/actions/workflow/status/supersheepbear/GeminiTeacher/main.yml?branch=main)](https://github.com/supersheepbear/GeminiTeacher/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/supersheepbear/GeminiTeacher/branch/main/graph/badge.svg)](https://codecov.io/gh/supersheepbear/GeminiTeacher)
[![License](https://img.shields.io/github/license/supersheepbear/GeminiTeacher)](https://img.shields.io/github/license/supersheepbear/GeminiTeacher)

**GeminiTeacher** is an AI-powered course creation toolkit using Google's Gemini LLM. It transforms raw text, markdown, or documents into structured, lesson-based educational content. Ideal for educators, developers, and content creators.

- **Full Documentation**: [https://supersheepbear.github.io/GeminiTeacher/](https://supersheepbear.github.io/GeminiTeacher/)
- **Source Code**: [https://github.com/supersheepbear/GeminiTeacher/](https://github.com/supersheepbear/GeminiTeacher/)

## Ways to Use GeminiTeacher

There are two primary ways to use GeminiTeacher, based on your preference.

| Method | Description | Best For |
| --- | --- | --- |
| 🚀 **GUI Application** | A user-friendly graphical interface with all options available. | Users who prefer a visual interface and easy controls. |
| 💻 **Command-Line (CLI)** | A powerful command-line tool for experts and automation. | Power users, developers, and integration into scripts. |

### Quick Start (GUI)

1.  **Installation**: All setup instructions are in the new [**Usage Guide**](./docs/usage.md).
2.  **Launch the App**: Run the following command in your terminal:
    ```bash
    uv run geminiteacher-gui
    ```
3.  **Generate**: Fill in the fields and click "Generate Course". See the full [**Usage Guide**](./docs/usage.md) for more details.

### Quick Start (CLI)

The command-line interface is best managed with a `config.yaml` file. Full instructions, including setup, are in the [**Usage Guide**](./docs/usage.md).

#### 1. Create a Configuration File

Create a `config.yaml` to define your settings.

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

#### 2. Run the Generator

Now, run the command from your terminal:

```bash
uv run python -m geminiteacher.app.generate_course --config config.yaml
```

The tool will create the specified output directory and fill it with structured markdown files for each chapter and a course summary.

## Key Features

- **Automated Course Structuring**: Intelligently organizes raw text into logical, lesson-based chapters.
- **Config-Driven Workflow**: Use a simple YAML file to control all aspects of course generation.
- **Parallel Processing**: Generates chapters concurrently to dramatically reduce creation time.
- **GUI & CLI**: Use the user-friendly graphical interface or the powerful command-line tool.
- **Customizable AI Behavior**: Use custom prompts and temperature controls to tailor the output to your needs.
- **Robust and Reliable**: Includes progressive saving and automatic retries for network errors.

## Learn More

For detailed instructions on all features, please see the full [**Usage Guide**](./docs/usage.md).

## Contributing

Contributions are welcome! Please check out our [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
