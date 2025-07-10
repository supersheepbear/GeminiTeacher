# Installation and Setup

This guide provides the steps to install GeminiTeacher and configure your environment.

## 1. Install the Package

Install GeminiTeacher directly from the Python Package Index (PyPI):

```bash
pip install geminiteacher
```

This command installs the package along with its command-line interface.

### Verifying the Installation

To verify that the command-line tool is properly installed, you can run:

```bash
uv run python -m geminiteacher.app.generate_course --help
```

If you see the help message, the installation was successful.

If the command is not found, your Python scripts directory might not be in your system's PATH. In that case, you can always run the tool using Python's module syntax:

```bash
python -m geminiteacher.app.generate_course --help
```

## 2. Set Up Your Google API Key

GeminiTeacher requires a Google API key with access to the Gemini family of models.

You must provide this key to the application. The recommended way is to set it as an environment variable, which keeps your key secure and out of your source code.

### For Linux/macOS

```bash
export GOOGLE_API_KEY="your-api-key-here"
```
To make this permanent, add the line to your `~/.bashrc`, `~/.zshrc`, or other shell configuration file.

### For Windows (PowerShell)

```powershell
$env:GOOGLE_API_KEY="your-api-key-here"
```
To make this permanent, add this line to your PowerShell profile script.

### For Windows (Command Prompt)

```batch
set GOOGLE_API_KEY=your-api-key-here
```

You can also place the key directly in a `config.yaml` file, but using an environment variable is best practice. 