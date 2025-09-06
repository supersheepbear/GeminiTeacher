# GeminiTeacher

GeminiTeacher is a Python application that uses Google's Gemini LLM to automatically generate structured learning courses from provided text content.

## Features

- Generate complete courses from text input
- Support for multiple file formats via the `markitdown` library
- Three generation modes:
  - **Sequential**: Generate chapters one after another (default)
  - **Parallel**: Generate chapters simultaneously for faster processing
  - **Cascade**: Generate chapters in sequence, with each new chapter building on previous ones
- Command-line interface (CLI)
- Graphical user interface (GUI)
- Progressive saving of generated content
- Customizable prompts and generation parameters

## Installation

```bash
pip install geminiteacher
```

Or install from source:

```bash
git clone https://github.com/yourusername/geminiteacher.git
cd geminiteacher
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Basic usage
geminiteacher --input content.txt --output-dir courses --title "My Course"

# With more options
geminiteacher --input content.txt --output-dir courses --title "My Course" \
  --max-chapters 5 --fixed-chapter-count --temperature 0.2 \
  --mode cascade --custom-prompt "Focus on practical examples"
```

### Graphical User Interface

```bash
# Launch the GUI
geminiteacher-gui
```

## Output Files

By default, the application saves generated files to:
- CLI: The directory specified with `--output-dir` (required)
- GUI: The directory specified in the "Output Directory" field, or `app/output` if left empty

Each course generation creates:
- One markdown file per chapter: `{course_title}_chapter_{nn}_{chapter_title}.md`
- One summary file: `{course_title}_summary.md`

## API Key

You need to provide a Google API key with access to the Gemini API:

1. Set the `GOOGLE_API_KEY` environment variable, or
2. Enter the API key in the GUI

## Documentation

For more detailed documentation, see the [docs](https://geminiteacher.readthedocs.io/).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
