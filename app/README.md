# Course Generator App

This application uses the CascadeLLM coursemaker module to generate structured educational courses from raw text content.

## Features

- Generate structured courses with chapters, explanations, and summaries
- **Process various file formats** including PDF, DOCX, PPTX, and more, by automatically converting them to Markdown
- Two chapter generation modes: adaptive (based on content complexity) or fixed count
- Configure API keys and model settings via YAML configuration
- Output course content as Markdown files
- Customize model parameters like temperature

## Setup

1.  **Install Dependencies**: This project uses `uv` for package management. To install all required dependencies, run the following command from the project's root directory:

    ```bash
    uv sync
    ```

2.  **Configure API Key**: Copy the `app/config.yaml_example` file to `app/config.yaml` and replace the placeholder with your actual Google Gemini API key.

    ```yaml
    # app/config.yaml
    api:
      google_api_key: "your_gemini_api_key_here"
    ```

## Supported Input Formats

Thanks to the integration of the `markitdown` library, this application can accept a wide variety of input file formats beyond plain text. The script will automatically detect the file type and convert it to Markdown before generating the course.

Supported formats include, but are not limited to:
-   PDF (`.pdf`)
-   Microsoft Word (`.docx`)
-   Microsoft PowerPoint (`.pptx`)
-   Microsoft Excel (`.xlsx`, `.xls`)
-   HTML (`.html`)
-   EPub (`.epub`)
-   And many other text-based formats.

For a full list of supported formats, please refer to the [markitdown documentation](https://github.com/microsoft/markitdown).

## Usage

To run the course generator, use the `uv run` command from the project root, followed by the path to the script and any desired arguments.

**Example with a PDF file:**
```bash
uv run python app/generate_course.py app/sample.pdf --title "My PDF Course"
```

**Example with a text file:**
```bash
uv run python app/generate_course.py app/sample_input.txt --title "AI Fundamentals"
```

### Command Line Arguments

- `input`: Path to the input content file (required)
- `--config`: Path to configuration file (default: `app/config.yaml`)
- `--title`: Title of the course (default: "Generated Course")
- `--verbose`, `-v`: Enable verbose output
- `--max-chapters`: Maximum number of chapters to generate (default: 10)
- `--fixed-chapters`: If set, generates exactly `--max-chapters` chapters instead of adapting based on content complexity.

### Chapter Generation Modes

The application supports two modes for chapter generation:

1.  **Adaptive Mode (Default)**: The AI analyzes the content and determines the optimal number of chapters (between 1 and `--max-chapters`) based on its complexity.

2.  **Fixed Mode**: The AI generates exactly the number of chapters specified by `--max-chapters`.

### Examples

```bash
# Adaptive mode (default) - generates between 1-10 chapters based on content complexity
uv run python app/generate_course.py app/sample_input.txt --title "Introduction to AI" --max-chapters 10

# Fixed mode - generates exactly 5 chapters
uv run python app/generate_course.py app/sample_input.txt --title "Introduction to AI" --max-chapters 5 --fixed-chapters
```

## Output

The generated course will be saved in the `app/output` directory (configurable in `config.yaml`) with the following structure:

- `{course_title}_summary.md`: Overall course summary
- `{course_title}_chapter_01.md`, `{course_title}_chapter_02.md`, etc.: Individual chapter files

Each chapter file includes:
- Chapter title
- Summary
- Detailed explanation
- Extension thoughts

## Configuration

You can customize the behavior by editing `app/config.yaml`:

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