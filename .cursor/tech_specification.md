# [AI_CONTEXT] Technical Specification: geminiteacher

## 1. Project High-Level Summary

*   **Purpose:** An educational content generation toolkit powered by Google's Gemini LLM.
*   **Core Dependencies:** `langchain`, `langchain-core`, `langchain-google-genai`, `pydantic`, `markitdown`, `pyyaml`, `PySide6`.
*   **Primary Entry Points:** `create_course()`, `create_course_parallel()`, `create_course_cascade()`, `geminiteacher.app.generate_course.main()`, `geminiteacher.gui.app.main()`.

---

## 2. Module & API Breakdown

### Module: `src/geminiteacher/app/generate_course.py`

*   **Purpose:** Provides a command-line application to generate courses from configuration files.
*   **Public API:**
    *   **Function `configure_logging(log_file=None, verbose=False) -> logging.Logger`**
        *   `// Description: Configure logging for the application.`
    *   **Function `load_config(config_path: str) -> Dict[str, Any]`**
        *   `// Description: Load configuration from a YAML file.`
    *   **Function `setup_environment(config: Dict[str, Any]) -> None`**
        *   `// Description: Set up environment variables from configuration.`
    *   **Function `read_input_content(input_path: str) -> str`**
        *   `// Description: Read content from an input file.`
    *   **Function `read_custom_prompt(file_path: str) -> str`**
        *   `// Description: Read custom prompt instructions from a file.`
    *   **Function `save_chapter_to_file(course_title: str, chapter: Any, chapter_index: int, output_dir: str) -> str`**
        *   `// Description: Save a single chapter to a file.`
    *   **Function `save_course_to_files(course_title: str, course_content: Course, output_dir: str) -> None`**
        *   `// Description: Save course content to files.`
    *   **Function `create_course_with_progressive_save(...) -> Course`**
        *   `// Description: Create a course and save each chapter as it's generated.`
    *   **Function `main()`**
        *   `// Description: Main function for the command-line application.`

### Module: `src/geminiteacher/converter.py`

*   **Purpose:** Converts document files (PDF, DOCX, etc.) to Markdown text.
*   **Public API:**
    *   **Function `convert_to_markdown(file_path: Union[str, Path], output_dir: Optional[str] = None) -> str`**
        *   `// Description: Convert a document file to Markdown text.`

### Module: `src/geminiteacher/coursemaker.py`

*   **Purpose:** Contains the core logic for the automated course generation system using an LLM.
*   **Public API:**
    *   **Class `ChapterContent(BaseModel)`**
        *   `// Description: A structured representation of a chapter's content.`
        *   `title: str`
        *   `summary: str`
        *   `explanation: str`
        *   `extension: str`
    *   **Class `Course(BaseModel)`**
        *   `// Description: A complete course with chapters and summary.`
        *   `content: str`
        *   `chapters: List[ChapterContent]`
        *   `summary: str`
    *   **Function `create_toc_prompt(max_chapters: int = 10, fixed_chapter_count: bool = False) -> ChatPromptTemplate`**
        *   `// Description: Create the prompt template for TOC generation.`
    *   **Function `create_chapter_prompt_template(custom_prompt: Optional[str] = None) -> ChatPromptTemplate`**
        *   `// Description: Create a prompt template for generating chapter explanations.`
    *   **Function `create_summary_prompt_template() -> ChatPromptTemplate`**
        *   `// Description: Create a prompt template for generating a course summary.`
    *   **Function `configure_gemini_llm(api_key: Optional[str] = None, model_name: str = "gemini-1.5-pro", temperature: float = 0.0) -> BaseLanguageModel`**
        *   `// Description: Configure and return a Google Gemini model.`
    *   **Function `get_default_llm(temperature: float = 0.0) -> BaseLanguageModel`**
        *   `// Description: Get the default LLM for this module (Google Gemini).`
    *   **Function `generate_toc(content: str, ..., fixed_chapter_count: bool = False) -> List[str]`**
        *   `// Description: Generate a table of contents from raw content.`
    *   **Function `generate_chapter(chapter_title: str, ..., custom_prompt: Optional[str] = None) -> ChapterContent`**
        *   `// Description: Generate a structured explanation for a single chapter.`
    *   **Function `generate_summary(content: str, ..., temperature: float = 0.0) -> str`**
        *   `// Description: Generate a comprehensive summary for the entire course.`
    *   **Function `create_course(content: str, ..., custom_prompt: Optional[str] = None) -> Course`**
        *   `// Description: Create a complete structured course from raw content.`
    *   **Function `parse_chapter_content(chapter_title: str, text: str) -> ChapterContent`**
        *   `// Description: Parse the raw text output from the LLM into structured chapter content.`
    *   **Function `create_course_parallel(...) -> Course`**
        *   `// Description: Create a course with parallel chapter generation.`
    *   **Function `create_course_cascade(...) -> Course`**
        *   `// Description: Create a course with cascade chapter generation.`

### Module: `src/geminiteacher/gui/app.py`

*   **Purpose:** The main entry point for the GUI application.
*   **Public API:**
    *   **Function `main()`**
        *   `// Description: The main entry point for the GUI application.`

### Module: `src/geminiteacher/gui/main_window.py`

*   **Purpose:** Defines the main window, widgets, and logic for the PySide6 GUI.
*   **Public API:**
    *   **Class `QtLogHandler(logging.Handler)`**
        *   `// Description: A logging handler that emits a Qt signal for each log record.`
    *   **Class `Worker(QObject)`**
        *   `// Description: A worker object that runs a long-running task in a separate thread.`
    *   **Class `MainWindow(QMainWindow)`**
        *   `// Description: The main application window for the GUI.`

### Module: `src/geminiteacher/parallel.py`

*   **Purpose:** Provides utilities for parallel processing of chapter generation.
*   **Public API:**
    *   **Function `generate_chapter_with_retry(...) -> ChapterContent`**
        *   `// Description: Generate a chapter with retry logic for handling API failures.`
    *   **Function `parallel_map_with_delay(func: Callable[..., T], ...) -> List[T]`**
        *   `// Description: Execute a function on multiple items in parallel with a delay between submissions.`
    *   **Function `save_chapter_to_file(...) -> str`**
        *   `// Description: Save a single chapter to a file.`
    *   **Function `parallel_generate_chapters(...) -> List[ChapterContent]`**
        *   `// Description: Generate multiple chapters in parallel with retry logic and rate limiting.`

# [END_AI_CONTEXT]