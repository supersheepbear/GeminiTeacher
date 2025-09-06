# Usage Guide

## Command Line Interface (CLI)

GeminiTeacher provides a command-line interface for easy integration into scripts and workflows.

### Basic Usage

```bash
geminiteacher --input content.txt --output-dir courses --title "My Course"
```

### Required Arguments

- `--input`: Path to the input file (text, PDF, DOCX, etc.)
- `--output-dir`: Directory where generated course files will be saved
- `--title`: Title of the course

### Optional Arguments

- `--temperature`: Temperature for LLM generation (default: 0.2)
- `--max-chapters`: Maximum number of chapters to generate (default: 10)
- `--fixed-chapter-count`: Generate exactly the number of chapters specified by --max-chapters
- `--custom-prompt`: Custom instructions for chapter generation or path to a file containing instructions
- `--model-name`: Model name to use (default: "gemini-1.5-pro")
- `--verbose`: Enable verbose logging
- `--log-file`: Path to log file
- `--config`: Path to YAML config file

### Generation Modes

- `--mode`: Choose the generation mode (default: "sequential")
  - `sequential`: Generate chapters one after another
  - `parallel`: Generate chapters simultaneously
  - `cascade`: Generate chapters sequentially, with each new chapter building on previous ones

### Parallel Processing Options

- `--parallel`: Enable parallel processing
- `--max-workers`: Maximum number of worker processes (default: CPU count)
- `--delay-min`: Minimum delay between API calls in seconds (default: 0.2)
- `--delay-max`: Maximum delay between API calls in seconds (default: 0.8)
- `--max-retries`: Maximum number of retries for failed API calls (default: 3)

### Example with All Options

```bash
geminiteacher \
  --input content.txt \
  --output-dir courses \
  --title "Advanced Python Programming" \
  --temperature 0.3 \
  --max-chapters 8 \
  --fixed-chapter-count \
  --custom-prompt "Focus on practical examples and include code snippets" \
  --model-name "gemini-1.5-pro" \
  --mode cascade \
  --verbose \
  --log-file generation.log
```

## Graphical User Interface (GUI)

GeminiTeacher also provides a user-friendly GUI for interactive use.

### Launching the GUI

```bash
geminiteacher-gui
```

### GUI Components

1. **API Key**: Enter your Google API Key (or set the GOOGLE_API_KEY environment variable)
2. **Input File**: Select the input file containing your content
3. **Output Directory**: Choose where to save the generated course files (defaults to `app/output` if left empty)
4. **Course Title**: Enter a title for your course
5. **Max Chapters**: Set the maximum number of chapters to generate
6. **Fixed Chapter Count**: Check to generate exactly the specified number of chapters
7. **Temperature**: Adjust the creativity of the LLM (0.0-1.0)
8. **Generation Mode**: Choose between Sequential, Parallel, or Cascade generation
9. **Parallel Processing Options**: Configure parallel processing settings
10. **Generate Course**: Click to start the generation process
11. **Open Output Directory**: Click to open the folder where files are saved

## Output Files

The application generates the following files in the output directory:

- `{course_title}_chapter_{nn}_{chapter_title}.md`: Individual chapter files
- `{course_title}_summary.md`: Course summary file

Each chapter file contains:
- Title
- Summary
- Detailed explanation
- Extension thoughts

## Generation Modes Explained

### Sequential Mode (Default)

In sequential mode, chapters are generated one after another, but each chapter is generated independently based only on the original content. This mode offers a good balance between speed and quality.

### Parallel Mode

In parallel mode, multiple chapters are generated simultaneously using multiple worker processes. This mode is significantly faster than sequential mode, but each chapter is still generated independently.

### Cascade Mode

In cascade mode, chapters are generated sequentially, with each new chapter being informed by the summaries of all previously generated chapters. This creates a more coherent narrative flow while avoiding content repetition.

**Key Features:**
- Each chapter is generated based on the original content plus summaries of previous chapters
- The AI receives explicit instructions not to repeat topics already covered
- Previous chapter summaries are used as a "what to avoid" guide
- This prevents content duplication while maintaining logical progression

**How it works:**
1. Generate the first chapter based only on the original content
2. For the second chapter, include a summary of Chapter 1 in the prompt with instructions to avoid repetition
3. For the third chapter, include summaries of Chapters 1 and 2, and so on
4. Each chapter builds upon previous knowledge without repeating content

Cascade mode is ideal for:
- Creating courses with a progressive learning path
- Ensuring consistent terminology throughout the course
- **Avoiding repetition of content between chapters** (primary benefit)
- Building upon concepts introduced in earlier chapters
- Creating a natural flow from basic to advanced topics

Note that cascade mode is always sequential and cannot be parallelized due to its dependency on previous chapters.

## API Key

You need to provide a Google API key with access to the Gemini API:

1. Set the `GOOGLE_API_KEY` environment variable, or
2. Enter the API key in the GUI or CLI

## Configuration File

You can use a YAML configuration file to store your preferred settings:

```yaml
api:
  model_name: "gemini-1.5-pro"

input:
  path: "content.txt"

output:
  directory: "courses"

course:
  title: "My Course"
  custom_prompt: "Focus on practical examples"

generation:
  temperature: 0.2
  max_chapters: 10
  fixed_chapter_count: true
  mode: "cascade"

parallel:
  enabled: false
  max_workers: 4
  delay_min: 0.2
  delay_max: 0.8
  max_retries: 3

logging:
  verbose: true
  log_file: "generation.log"
```

Use the configuration file with:

```bash
geminiteacher --config config.yaml
```

Command-line arguments will override values in the configuration file. 