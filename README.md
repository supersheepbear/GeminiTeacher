# GeminiTeacher: The AI-Powered Course Creator

Turn any text-based document (notes, articles, books) into a structured, multi-chapter online course with a single command.

GeminiTeacher acts like an AI agent, using a sequence of cascading prompts with Google's Gemini models to perform a comprehensive analysis of your content. It intelligently outlines a table of contents, then generates a detailed chapter and a final summary for each part, effectively creating a full book from your raw material.

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

For detailed instructions on all features, including how to use **custom instruction files** to guide the AI's tone and style, please see the full [**Usage Guide**](./docs/usage.md).

## Contributing

Contributions are welcome! Please check out our [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
