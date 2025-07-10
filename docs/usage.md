# Usage Guide

This guide covers the primary ways to use GeminiTeacher, from the simple command-line interface (CLI) to the flexible Python API.

For setup instructions, please see the [**Installation and Setup**](installation.md) guide first.

## Command-Line Usage (Recommended)

The easiest and most powerful way to use GeminiTeacher is through its command-line interface, which is ideal for generating courses without writing any code. We recommend using a configuration file for the best experience.

### Method 1: Using a `config.yaml` File (Best Practice)

Create a `config.yaml` file to manage all your settings in one place. This is the most organized and repeatable way to generate courses.

1.  **Create a `config.yaml` file:**

    Here is an example `config.yaml`:
    ```yaml
    # --- Input/Output Settings ---
    input:
      # Path to your raw content file. This can be any text-based format
      # that Python can read, such as .txt, .md, .rst, .py, etc.
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
    uv run python -m geminiteacher.app.generate_course --config config.yaml
    ```

### Method 2: Using Command-Line Flags

You can also control the generation process directly with command-line arguments. These are useful for quick, one-off tasks.

```bash
# Basic usage with a text file
uv run python -m geminiteacher.app.generate_course --input content.txt --output-dir courses --title "Machine Learning Basics"

# Enable parallel processing for faster generation
uv run python -m geminiteacher.app.generate_course --input content.txt --parallel --max-workers 4

# Use a custom prompt file and set the temperature
uv run python -m geminiteacher.app.generate_course --input content.txt --custom-prompt prompts.txt --temperature 0.3
```

### All Command-Line Options

Here is the full list of available command-line options. Any option passed as a flag will override the corresponding value in a `config.yaml` file.

| Option                  | Alias | Type      | Description                                                                                                                              |
| ----------------------- | ----- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `--config`              | `-c`  | `PATH`    | Path to the YAML configuration file. If used, all other options can be defined here.                                                     |
| `--input`               | `-i`  | `PATH`    | **Required.** Path to the input content file (e.g., `.txt`, `.md`).                                                                       |
| `--output-dir`          | `-o`  | `PATH`    | **Required.** Directory where the generated course files will be saved.                                                                  |
| `--title`               | `-t`  | `TEXT`    | **Required.** The title of your course.                                                                                                  |
| `--custom-prompt`       | `-p`  | `PATH`    | Optional path to a file containing custom instructions for the AI to follow during generation.                                           |
| `--model-name`          |       | `TEXT`    | The specific Gemini model to use (e.g., `gemini-1.5-pro`, `gemini-2.5-flash`). Default: `gemini-1.5-pro`.                                    |
| `--temperature`         |       | `FLOAT`   | Controls the "creativity" or randomness of the AI's output. A value from `0.0` (most predictable) to `1.0` (most creative). Default: `0.2`. |
| `--max-chapters`        |       | `INTEGER` | The target number of chapters for the course. The final number may be less if the AI deems it appropriate. Default: `10`.                |
| `--fixed-chapter-count` |       | `FLAG`    | If set, forces the AI to generate exactly the number of chapters specified by `--max-chapters`.                                          |
| `--parallel`            |       | `FLAG`    | If set, enables parallel processing to generate chapters simultaneously for a significant speed boost.                                   |
| `--max-workers`         |       | `INTEGER` | When using `--parallel`, this sets the number of concurrent processes. Defaults to the number of CPU cores on your machine.              |
| `--delay-min`           |       | `FLOAT`   | The minimum random delay (in seconds) between parallel API requests to avoid rate limiting. Default: `0.2`.                              |
| `--delay-max`           |       | `FLOAT`   | The maximum random delay (in seconds) between parallel API requests. Default: `0.8`.                                                     |
| `--max-retries`         |       | `INTEGER` | The maximum number of times to retry a failed API call for a chapter before giving up. Default: `3`.                                     |
| `--verbose`             | `-v`  | `FLAG`    | Enable verbose output for detailed real-time progress logging, which is very helpful for debugging.                                    |
| `--log-file`            |       | `PATH`    | Optional path to a file where all log output will be saved.                                                                              |

### Advanced "Power User" Example

Here is an example of a command that uses multiple flags for fine-grained control over the generation process. This is useful for large, important documents where you want to maximize speed and quality.

```bash
uv run python -m geminiteacher.app.generate_course \
  --input "input/xianxingdaishu.md" \
  --output-dir "output/linear_algebra_course" \
  --title "Linear Algebra Fundamentals" \
  --custom-prompt "input/xianxingdaishu_prompt.txt" \
  --max-chapters 10 \
  --fixed-chapter-count \
  --parallel \
  --max-workers 14 \
  --delay-min 0.2 \
  --delay-max 1.0 \
  --max-retries 5 \
  --verbose
```

**What this command does:**
- **`--input "input/xianxingdaishu.md"`**: Specifies the source material.
- **`--output-dir "output/linear_algebra_course"`**: Sets the destination for the course files.
- **`--title "Linear Algebra Fundamentals"`**: Gives the course a clear title.
- **`--custom-prompt "input/xianxingdaishu_prompt.txt"`**: Uses a dedicated prompt file to guide the AI's tone and style.
- **`--max-chapters 10 --fixed-chapter-count`**: Instructs the AI to generate exactly 10 chapters.
- **`--parallel --max-workers 14`**: Enables high-speed generation using 14 parallel processes.
- **`--delay-min 0.2 --delay-max 1.0`**: Adds a random delay of 0.2 to 1.0 seconds between API calls to prevent overwhelming the server.
- **`--max-retries 5`**: If an API call for a chapter fails, it will be retried up to 5 times.
- **`--verbose`**: Prints detailed logs to the console so you can monitor the progress in real-time.

### Troubleshooting the CLI

**"command not found" error?**

This can happen if your Python scripts directory is not in your system's `PATH`. The most reliable way to run the application is always by using `uv run`, as shown in the examples above. See the [installation guide](installation.md) for more details.

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