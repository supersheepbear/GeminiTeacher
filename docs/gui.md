# Graphical User Interface (GUI) Guide

For a user-friendly experience without needing to use the command line, GeminiTeacher provides a simple graphical interface. It's the recommended way for most users to generate courses.

## Launching the GUI

After installing the project dependencies, you can launch the application with the following command:

```bash
uv run geminiteacher-gui
```

The main window will appear, giving you access to all of the course generation settings.

![GeminiTeacher GUI Screenshot](https://raw.githubusercontent.com/supersheepbear/GeminiTeacher/main/docs/assets/gui_screenshot.png)

## Features

### 1. Simple Input Fields

All the options available on the command line are present in the GUI with easy-to-use inputs:
- **API Key & Model**: Enter your Google API key and specify the Gemini model you wish to use (defaults to `gemini-2.5-flash`).
- **File Paths**: Use the "Browse..." buttons to easily select your input file, output directory, and optional custom prompt file.
- **Course & Generation Settings**: Adjust the course title, number of chapters, and AI temperature using simple controls.
- **Parallel Processing**: Enable or disable parallel generation and fine-tune performance settings like the number of workers and API retries.

### 2. Settings Caching

Your settings (including the API key, model name, and file paths) are automatically saved when you close the application and reloaded the next time you open it, saving you from re-entering information.

### 3. Real-time Progress and Logging

During course generation, you can monitor the progress in real-time:
- **Progress Bar**: The progress bar at the bottom gives you an at-a-glance view of the overall completion status.
- **Log Window**: A detailed log of the generation process is displayed in the text box. This is useful for seeing exactly what the tool is doing and for diagnosing any issues.

### 4. Responsive Interface

The course generation runs in a separate background thread, meaning the GUI will remain responsive and will not freeze, even when generating large courses. You can move or minimize the window while it's working. 