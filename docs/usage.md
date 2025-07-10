# Usage Guide

This guide covers the primary ways to use GeminiTeacher, from the simple command-line interface (CLI) to the flexible Python API.

For setup instructions, please see the [**Installation and Setup**](installation.md) guide first.

## Command-Line Usage (Recommended)

The easiest and most powerful way to use GeminiTeacher is through its command-line interface, which is ideal for generating courses without writing any code. We recommend using a configuration file for the best experience.

### Method 1: Using a `config.yaml` File (Best Practice)

Create a `config.yaml` file to manage all your settings in one place. This is the most organized and repeatable way to generate courses.

1.  **Create a `config.yaml` file:**

    ```yaml
    # config.yaml

    # --- Input/Output Settings ---
    input:
      # Path to your raw content file (e.g., a text file with your notes).
      path: "input/content.txt"
    output:
      # Directory where the generated course files will be saved.
      directory: "output/MyFirstCourse"

    # --- Course Settings ---
    course:
      # The title of your course.
      title: "Introduction to Artificial Intelligence"
      # Optional: Path to a file with custom instructions for the AI.
      custom_prompt: "prompts/formal_tone_prompt.txt"

    # --- Generation Settings ---
    generation:
      # Controls the "creativity" of the AI. Lower is more predictable. (0.0-1.0)
      temperature: 0.2
      # The target number of chapters for the course.
      max_chapters: 8
      # If true, the AI will generate exactly `max_chapters`.
      fixed_chapter_count: true

    # --- Performance Settings ---
    parallel:
      # Enable parallel processing to generate chapters simultaneously for speed.
      enabled: true
      # Number of parallel processes to run. Defaults to your CPU count.
      max_workers: 4
    ```

2.  **Run the command:**

    Simply point the CLI to your configuration file.

    ```bash
    geminiteacher --config config.yaml
    ```

### Method 2: Using Command-Line Flags

You can also control the generation process directly with command-line arguments. These are useful for quick, one-off tasks.

```bash
# Basic usage with a text file
geminiteacher --input content.txt --output-dir courses --title "Machine Learning Basics"

# Enable parallel processing for faster generation
geminiteacher --input content.txt --parallel --max-workers 4

# Use a custom prompt file and set the temperature
geminiteacher --input content.txt --custom-prompt prompts.txt --temperature 0.3
```

### All Command-Line Options

Here is the full list of available command-line options. Any option passed as a flag will override the corresponding value in a `config.yaml` file.

| Option                  | Argument        | Description                                                 |
| ----------------------- | --------------- | ----------------------------------------------------------- |
| `--config`, `-c`        | `PATH`          | Path to the YAML configuration file.                        |
| `--input`, `-i`         | `PATH`          | Path to the input content file.                             |
| `--output-dir`, `-o`    | `PATH`          | Directory to save generated course files.                   |
| `--title`, `-t`         | `TEXT`          | Course title.                                               |
| `--custom-prompt`, `-p` | `PATH`          | Path to a custom prompt instructions file.                  |
| `--temperature`         | `FLOAT`         | Temperature for generation (0.0-1.0).                       |
| `--max-chapters`        | `INTEGER`       | Maximum number of chapters to generate.                     |
| `--fixed-chapter-count` | *(flag)*        | If set, generates exactly `max-chapters`.                   |
| `--parallel`            | *(flag)*        | If set, use parallel processing for chapter generation.     |
| `--max-workers`         | `INTEGER`       | Max worker processes for parallel generation.               |
| `--verbose`, `-v`       | *(flag)*        | Enable verbose output for detailed progress logging.        |
| `--log-file`            | `PATH`          | Optional path to a file to save logs.                       |

### Troubleshooting the CLI

**"command not found" error?**

If your shell cannot find the `geminiteacher` command, you can run it directly as a Python module:

```bash
python -m geminiteacher.app.generate_course --config config.yaml
```

This happens when your Python scripts directory is not in your system's `PATH`. See the [installation guide](installation.md) for more details.

**API Key Errors?**

If you get authentication errors, ensure your `GOOGLE_API_KEY` is set correctly as an environment variable, as described in the [installation guide](installation.md).

## Python API Usage

For programmatic use, you can import GeminiTeacher directly into your Python code.

### High-Level Functions (Recommended)

The easiest way to use the API is with the `create_course` and `create_course_parallel` functions.

#### Sequential Generation

This is the simplest method, generating one component at a time.

```python
import geminiteacher as gt

# Your raw content to transform into a course
with open("content.txt", "r") as f:
    content = f.read()

# Generate the full course structure
course = gt.create_course(
    content=content,
    max_chapters=5,
    temperature=0.2
)

# Print the generated course structure
print(f"Course Summary: {course.summary}\n")
for chapter in course.chapters:
    print(f"- {chapter.title}")
```

#### Parallel Generation for Speed

Use `create_course_parallel` for large documents to significantly speed up chapter generation.

```python
import geminiteacher as gt

with open("content.txt", "r") as f:
    content = f.read()

# Generate a course with chapters created in parallel
# This also saves chapters to disk as they complete
course = gt.create_course_parallel(
    content=content,
    course_title="My Parallel Course",
    output_dir="courses_output",
    max_chapters=10,
    max_workers=4
)

print(f"Generated {len(course.chapters)} chapters in parallel.")
```

### Using Individual Components

For maximum control, you can use the individual functions from the generation pipeline.

```python
from geminiteacher import (
    configure_gemini_llm, 
    generate_toc, 
    generate_chapter, 
    generate_summary
)

# 1. Configure the LLM
llm = configure_gemini_llm(temperature=0.1)

# 2. Generate the Table of Contents
chapter_titles = generate_toc(content, llm=llm, max_chapters=5)

# 3. Generate each chapter individually
chapters = [
    generate_chapter(title, content, llm=llm) 
    for title in chapter_titles
]

# 4. Generate the final summary
summary = generate_summary(content, chapters, llm=llm)

print("Course generation complete!")
``` 