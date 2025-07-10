# GeminiTeacher

[![PyPI version](https://badge.fury.io/py/geminiteacher.svg)](https://badge.fury.io/py/geminiteacher)
[![Build status](https://img.shields.io/github/actions/workflow/status/supersheepbear/GeminiTeacher/main.yml?branch=main)](https://github.com/supersheepbear/GeminiTeacher/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/supersheepbear/GeminiTeacher/branch/main/graph/badge.svg)](https://codecov.io/gh/supersheepbear/GeminiTeacher)
[![License](https://img.shields.io/github/license/supersheepbear/GeminiTeacher)](https://img.shields.io/github/license/supersheepbear/GeminiTeacher)

**GeminiTeacher** is an educational content generation toolkit powered by Google's Gemini LLM. It transforms raw text content into structured, well-organized educational courses with minimal effort. Perfect for educators, content creators, and anyone looking to quickly create high-quality learning materials.

- **Documentation**: [https://supersheepbear.github.io/GeminiTeacher/](https://supersheepbear.github.io/GeminiTeacher/)
- **Source Code**: [https://github.com/supersheepbear/GeminiTeacher/](https://github.com/supersheepbear/GeminiTeacher/)

## Installation

Install GeminiTeacher directly from PyPI:

```bash
pip install geminiteacher
```

You'll need a Google API key with access to Gemini models. Set it as an environment variable:

```bash
# For Linux/macOS
export GOOGLE_API_KEY="your-api-key-here"

# For Windows (Command Prompt)
set GOOGLE_API_KEY=your-api-key-here

# For Windows (PowerShell)
$env:GOOGLE_API_KEY="your-api-key-here"
```

## Command-line Usage

After installation, you can immediately use the `geminiteacher` command-line tool:

```bash
# Basic usage with a text file
geminiteacher --input content.txt --output-dir courses --title "Machine Learning Basics"

# Enable parallel processing for faster generation
geminiteacher --input content.txt --parallel --max-workers 4

# Use a configuration file for more control
geminiteacher --config config.yaml
```

### Configuration File

Create a `config.yaml` file for more control over the generation process:

```yaml
# API Configuration
api:
  google_api_key: "your_gemini_api_key_here"  # Or use environment variable
  model_name: "gemini-1.5-pro"

# Input/Output Settings
input:
  path: "input/content.txt"  # Path to your content file

output:
  directory: "output"        # Where to save generated files

# Course Settings
course:
  title: "Machine Learning"  # Title of your course
  custom_prompt: "custom_instructions.txt"  # Optional custom prompt

# Generation Settings
generation:
  temperature: 0.2          # Controls randomness (0.0-1.0)
  max_chapters: 10          # Maximum number of chapters
  fixed_chapter_count: false # Generate exactly max_chapters?

# Parallel Processing Settings
parallel:
  enabled: true             # Use parallel processing?
  max_workers: 4            # Number of parallel workers
  delay_min: 0.2            # Min delay between API calls (seconds)
  delay_max: 0.8            # Max delay between API calls (seconds)
  max_retries: 3            # Max retry attempts for failed requests
```

For more details on command-line usage, see the [CLI Application documentation](https://supersheepbear.github.io/GeminiTeacher/app/).

## Python API Usage

Generate a complete course with just a few lines of code:

```python
import geminiteacher as gt

# Your raw content to transform into a course
content = """
Machine learning is a subfield of artificial intelligence that focuses on developing 
systems that can learn from and make decisions based on data. Unlike traditional 
programming where explicit instructions are provided, machine learning algorithms 
build models based on sample data to make predictions or decisions without being 
explicitly programmed to do so.
"""

# Generate a course with parallel processing for speed
course = gt.create_course_parallel(
    content=content,
    max_chapters=5,          # Maximum number of chapters to generate
    fixed_chapter_count=True,  # Generate exactly 5 chapters
    temperature=0.2,         # Control creativity (0.0-1.0)
    verbose=True             # Show progress messages
)

# Print the generated course structure
print(f"Course Summary: {course.summary}\n")
print(f"Generated {len(course.chapters)} chapters:")
for i, chapter in enumerate(course.chapters):
    print(f"  {i+1}. {chapter.title}")
```

### Using the App Module Programmatically

For more control and features like progressive saving:

```python
from geminiteacher.app import create_course_with_progressive_save, configure_logging

# Configure logging
logger = configure_logging(log_file="generation.log", verbose=True)

# Generate a course with progressive saving
course = create_course_with_progressive_save(
    content="Your content here...",
    course_title="Python Programming",
    output_dir="courses",
    temperature=0.2,
    max_chapters=5,
    custom_prompt="Focus on practical examples",
    verbose=True,
    logger=logger
)
```

## Key Features

- **Command-line Interface**: Generate courses without writing any code
- **Intelligent Content Organization**: Automatically structures content into logical chapters
- **Adaptive or Fixed Chapter Generation**: Let the AI determine the optimal number of chapters or specify exactly how many you want
- **Parallel Processing**: Generate chapters concurrently for significantly faster course creation
- **Custom Prompting**: Tailor the generation process with custom instructions
- **Progressive Saving**: Each chapter is saved as it's generated, ensuring no work is lost
- **Robust Error Handling**: Automatic retries with exponential backoff for API failures

## Advanced Usage

### Custom Prompts

Add specific instructions to guide the content generation:

```python
custom_prompt = "Focus on practical examples and include code snippets where relevant."

course = gt.create_course(
    content=content,
    custom_prompt=custom_prompt,
    temperature=0.3
)
```

### Parallel Processing with Custom Settings

Fine-tune the parallel processing behavior:

```python
course = gt.create_course_parallel(
    content=content,
    max_workers=4,              # Number of parallel workers
    delay_range=(0.2, 0.8),     # Random delay between API calls (seconds)
    max_retries=5,              # Maximum retry attempts for failed requests
    course_title="ML_Basics",   # Title for saved course files
    output_dir="courses"        # Directory to save generated chapters
)
```

## Contributing

Contributions are welcome! Please check out our [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ using Google Gemini and LangChain.
