# [AI_CONTEXT] Technical Specification: geminiteacher

## 1. Project High-Level Summary

* **Purpose:** An application to automatically generate structured learning courses from provided text content using Large Language Models, with support for both a command-line interface and a graphical user interface.
* **Core Dependencies:** `langchain`, `langchain-google-genai`, `pydantic`, `markitdown`, `pyyaml`, `PySide6`.
* **Primary Entry Points:** `create_course()`, `create_course_parallel()`, `geminiteacher` (CLI script), `geminiteacher-gui` (GUI app).

---

## 2. Module & API Breakdown

### Module: `src/geminiteacher/converter.py`

* **Purpose:** Transforms different document file formats (PDF, DOCX, etc.) into Markdown.
* **Public API:**
    * **Function `convert_to_markdown(file_path: Union[str, Path], output_dir: Optional[str] = None) -> str`**
        * `// Description: Converts a document file to Markdown text using the markitdown library.`

### Module: `src/geminiteacher/coursemaker.py`

* **Purpose:** Contains the core logic for the automated course generation system.
* **Public API:**
    * **Class `ChapterContent(BaseModel)`**
        * `// Description: A structured representation of a chapter's content (title, summary, explanation).`
    * **Class `Course(BaseModel)`**
        * `// Description: A representation of a complete course, containing the original content and a list of chapters.`
    * **Function `create_toc_prompt(max_chapters: int = 10, fixed_chapter_count: bool = False) -> ChatPromptTemplate`**
        * `// Description: Creates a LangChain prompt template for generating a table of contents.`
    * **Function `create_chapter_prompt_template(custom_prompt: Optional[str] = None) -> ChatPromptTemplate`**
        * `// Description: Creates a LangChain prompt template for generating detailed chapter content.`
    * **Function `create_summary_prompt_template() -> ChatPromptTemplate`**
        * `// Description: Creates a LangChain prompt template for generating a course summary.`
    * **Function `configure_gemini_llm(api_key: Optional[str] = None, model_name: str = "gemini-1.5-pro", temperature: float = 0.0) -> BaseLanguageModel`**
        * `// Description: Configures and returns an instance of a Google Gemini language model.`
    * **Function `generate_toc(content: str, ...) -> List[str]`**
        * `// Description: Generates a table of contents from the given text content using an LLM.`
    * **Function `generate_chapter(chapter_title: str, content: str, ...) -> ChapterContent`**
        * `// Description: Generates the detailed content for a single chapter based on its title.`
    * **Function `generate_summary(content: str, chapters: List[ChapterContent], ...) -> str`**
        * `// Description: Generates a comprehensive summary for the entire course.`
    * **Function `create_course(content: str, ...) -> Course`**
        * `// Description: Sequentially orchestrates the entire course creation process.`
    * **Function `parse_chapter_content(chapter_title: str, text: str) -> ChapterContent`**
        * `// Description: Parses the raw text output from an LLM into a structured ChapterContent object.`
    * **Function `create_course_parallel(content: str, ...) -> Course`**
        * `// Description: Orchestrates the entire course creation process using parallel execution for chapter generation.`

### Module: `src/geminiteacher/parallel.py`

* **Purpose:** Provides utilities for parallel processing to accelerate course generation.
* **Public API:**
    * **Function `generate_chapter_with_retry(...) -> ChapterContent`**
        * `// Description: A wrapper for `generate_chapter` that includes exponential backoff retry logic.`
    * **Function `parallel_map_with_delay(...) -> List[T]`**
        * `// Description: Executes a function over a list of items in parallel using a ProcessPoolExecutor, with a configurable delay.`
    * **Function `save_chapter_to_file(course_title: str, chapter: ChapterContent, chapter_index: int, output_dir: str) -> str`**
        * `// Description: Saves a single chapter's content to a formatted Markdown file.`
    * **Function `parallel_generate_chapters(...) -> List[ChapterContent]`**
        * `// Description: Manages the parallel generation of all course chapters, handling workers and saving results.`

### Module: `src/geminiteacher/app/generate_course.py`

* **Purpose:** Provides the command-line interface (CLI) for the course generation application.
* **Public API:**
    * **Function `configure_logging(log_file=None, verbose=False)`**
        * `// Description: Sets up application-wide logging to the console and optionally a file.`
    * **Function `load_config(config_path: str) -> Dict[str, Any]`**
        * `// Description: Loads application settings from a specified YAML file.`
    * **Function `create_course_with_progressive_save(...) -> Course`**
        * `// Description: An end-to-end function that generates a course and saves each chapter to a file as it's completed.`
    * **Function `main()`**
        * `// Description: The main entry point for the CLI, handling argument parsing and orchestrating the generation process.`

### Module: `src/geminiteacher/gui/app.py`

* **Purpose:** The main entry point for launching the GUI application.
* **Public API:**
    * **Function `main()`**
        * `// Description: Initializes and runs the PySide6 Qt application event loop.`

### Module: `src/geminiteacher/gui/main_window.py`

* **Purpose:** Defines the main window, UI components, and event handling for the GUI application.
* **Public API:**
    * **Class `QtLogHandler(logging.Handler)`**
        * `// Description: A custom logging handler to redirect log messages to a Qt widget.`
    * **Class `Worker(QObject)`**
        * `// Description: A QObject that runs the course generation task in a background thread to keep the GUI responsive.`
    * **Class `MainWindow(QMainWindow)`**
        * `// Description: The main application window class, responsible for building the UI and connecting signals/slots.`

# [END_AI_CONTEXT]