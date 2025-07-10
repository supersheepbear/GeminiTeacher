# Command-line Application

GeminiTeacher includes a powerful command-line application that makes it easy to generate courses without writing any code.

## Installation

The command-line application is installed automatically when you install the GeminiTeacher package:

```bash
pip install geminiteacher
```

After installation, the `geminiteacher` command should be available in your terminal. If the command is not found, make sure your Python scripts directory is in your PATH.

### Verifying Installation

To verify that the command-line tool is properly installed:

```bash
# Check if the command is available
geminiteacher --help

# If the command is not found, you can run it using Python's module syntax:
python -m geminiteacher.app.generate_course --help
```

### Setting Up Your API Key

Before using the tool, you must set up your Google API key:

```bash
# For Linux/macOS
export GOOGLE_API_KEY=your_api_key_here

# For Windows (Command Prompt)
set GOOGLE_API_KEY=your_api_key_here

# For Windows (PowerShell)
$env:GOOGLE_API_KEY="your_api_key_here"
```

Alternatively, you can specify the API key in your configuration file.

## Basic Usage

### Quick Start

Generate a course with minimal configuration:

```bash
# Generate a course from a text file
geminiteacher --input content.txt --title "Introduction to Python" --output-dir courses

# Alternative syntax if the command is not in your PATH
python -m geminiteacher.app.generate_course --input content.txt --title "Introduction to Python" --output-dir courses
```

### Using a Configuration File

For more control, create a `config.yaml` file:

```yaml
# API Configuration
api:
  google_api_key: "your_gemini_api_key_here"
  model_name: "gemini-1.5-pro"

# Input/Output Settings
input:
  path: "input/content.txt"

output:
  directory: "output"

# Course Settings
course:
  title: "My Course"
  custom_prompt: "custom_instructions.txt"

# Generation Settings
generation:
  temperature: 0.2
  max_chapters: 10
  fixed_chapter_count: false

# Parallel Processing Settings
parallel:
  enabled: true
  max_workers: 4
  delay_min: 0.2
  delay_max: 0.8
  max_retries: 3
```

Then run:

```bash
geminiteacher --config config.yaml

# Alternative syntax
python -m geminiteacher.app.generate_course --config config.yaml
```

## Command-line Options

The application supports the following command-line options:

| Option | Description |
|--------|-------------|
| `--config`, `-c` | Path to configuration file |
| `--input`, `-i` | Path to input content file |
| `--output-dir`, `-o` | Directory to save generated course files |
| `--title`, `-t` | Course title |
| `--custom-prompt`, `-p` | Path to custom prompt instructions file |
| `--temperature` | Temperature for generation (0.0-1.0) |
| `--max-chapters` | Maximum number of chapters |
| `--fixed-chapter-count` | Generate exactly max-chapters chapters |
| `--parallel` | Use parallel processing for chapter generation |
| `--max-workers` | Maximum number of worker processes for parallel generation |
| `--verbose`, `-v` | Enable verbose output |
| `--log-file` | Path to log file |

## Custom Prompts

You can customize the generation process by providing a custom prompt file. This file should contain instructions for the LLM about how to generate the course content.

Example custom prompt file:

```
Focus on practical examples and include code snippets where relevant.
Each concept should be explained with a real-world application.
Include exercises at the end of each explanation section.
```

Use it with:

```bash
geminiteacher --input content.txt --custom-prompt custom_instructions.txt
```

## Output Structure

The application generates the following files in the output directory:

- `{course_title}_chapter_{nn}_{chapter_title}.md` - Individual chapter files
- `{course_title}_summary.md` - Course summary file

Each chapter file contains:
- Title
- Summary
- Detailed explanation
- Extension thoughts

## Troubleshooting

### Command Not Found

If you encounter a "command not found" error:

1. Make sure you've installed the package correctly:
   ```bash
   pip install --upgrade geminiteacher
   ```

2. Use the Python module syntax instead:
   ```bash
   python -m geminiteacher.app.generate_course --input content.txt
   ```

3. Check if your Python scripts directory is in your PATH:
   ```bash
   # Find your Python scripts directory
   python -c "import site; print(site.USER_BASE + '/bin')"  # Linux/macOS
   python -c "import site; print(site.USER_BASE + '\\Scripts')"  # Windows
   ```

### API Key Issues

If you encounter authentication errors:

1. Verify your API key is set correctly:
   ```bash
   # Linux/macOS
   echo $GOOGLE_API_KEY
   
   # Windows (Command Prompt)
   echo %GOOGLE_API_KEY%
   
   # Windows (PowerShell)
   echo $env:GOOGLE_API_KEY
   ```

2. Ensure your API key has access to Gemini models.

3. Try specifying the API key directly in your config.yaml file.

## Programmatic Usage

You can also use the app module programmatically in your Python code:

```python
from geminiteacher.app import create_course_with_progressive_save, configure_logging

# Configure logging
logger = configure_logging(log_file="generation.log", verbose=True)

# Generate a course
course = create_course_with_progressive_save(
    content="Your content here...",
    course_title="Python Programming",
    output_dir="courses",
    temperature=0.2,
    max_chapters=5,
    fixed_chapter_count=True,
    custom_prompt="Focus on practical examples",
    verbose=True,
    logger=logger
)

# Access the generated course
print(f"Generated {len(course.chapters)} chapters")
for i, chapter in enumerate(course.chapters):
    print(f"Chapter {i+1}: {chapter.title}")
``` 