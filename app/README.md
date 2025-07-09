# Course Generator App

This application uses the CascadeLLM coursemaker module to generate structured educational courses from raw text content.

## Features

- Generate structured courses with chapters, explanations, and summaries
- Configure API keys and model settings via YAML configuration
- Output course content as Markdown files
- Customize model parameters like temperature

## Setup

1. Install the required dependencies:

```bash
pip install pyyaml
```

2. Configure your API key in `config.yaml`:

```yaml
api:
  google_api_key: "your_gemini_api_key_here"  # Replace with your actual API key
```

## Usage

```bash
python generate_course.py sample_input.txt --title "AI Fundamentals"
```

### Command Line Arguments

- `input`: Path to the input content file (required)
- `--config`: Path to configuration file (default: config.yaml)
- `--title`: Title of the course (default: "Generated Course")

### Example

```bash
python generate_course.py sample_input.txt --title "Introduction to AI" --config custom_config.yaml
```

## Output

The generated course will be saved in the `output` directory (configurable in `config.yaml`) with the following structure:

- `{course_title}_summary.md`: Overall course summary
- `{course_title}_chapter_01.md`, `{course_title}_chapter_02.md`, etc.: Individual chapter files

Each chapter file includes:
- Chapter title
- Summary
- Detailed explanation
- Extension thoughts

## Configuration

You can customize the behavior by editing `config.yaml`:

```yaml
# Gemini API Configuration
api:
  google_api_key: "your_gemini_api_key_here"

# Model Settings
model:
  name: "gemini-1.5-pro"  # Model name
  temperature: 0.2        # Controls randomness (0.0 to 1.0)

# Course Generation Settings
course:
  output_dir: "output"    # Directory to save generated courses
``` 