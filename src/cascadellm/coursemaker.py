"""This module contains the logic for the automated course generation system."""
from typing import List, Dict, Any, Optional, Union

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.language_models import BaseLanguageModel
from pydantic import BaseModel, Field


class ChapterContent(BaseModel):
    """
    A structured representation of a chapter's content.
    
    Attributes
    ----
    title : str
        The title of the chapter.
    summary : str
        A brief summary or introduction to the chapter.
    explanation : str
        The detailed explanation of the chapter's content.
    extension : str
        Additional thoughts or extensions related to the chapter.
    """
    
    title: str
    summary: str = ""
    explanation: str = ""
    extension: str = ""


class Course(BaseModel):
    """
    A complete course with chapters and summary.
    
    Attributes
    ----
    content : str
        The original raw content used to generate the course.
    chapters : List[ChapterContent]
        The list of chapters in the course.
    summary : str
        A comprehensive summary of the entire course.
    """
    
    content: str
    chapters: List[ChapterContent] = []
    summary: str = ""


def create_toc_prompt() -> ChatPromptTemplate:
    """
    Create the prompt template for TOC generation.
    
    Returns
    ----
    ChatPromptTemplate
        A prompt template for generating a table of contents.
    """
    return ChatPromptTemplate.from_template(
        """You are a professional educator creating a structured learning curriculum.
        
        Below is raw content that needs to be organized into a meaningful table of contents.
        Create a logical structure with 1-10 chapter titles in simplified Chinese.
        Format your response as a numbered list, with each chapter on a new line.
        
        DO NOT include any explanations, introductions, or additional text.
        ONLY include the numbered list of chapter titles.
        
        Raw content:
        {content}
        """
    )


def create_chapter_prompt_template() -> ChatPromptTemplate:
    """
    Create a prompt template for generating chapter explanations.
    
    This template instructs the LLM to generate a structured explanation
    for a single chapter, based on its title and the original content.
    
    Returns
    ----
    ChatPromptTemplate
        A prompt template for generating chapter explanations.
    
    Examples
    -----
    >>> prompt = create_chapter_prompt_template()
    >>> prompt.format(chapter_title="Introduction to AI", content="...")
    """
    return ChatPromptTemplate.from_template(
        """你是一位专业教育工作者，正在创建一个结构化的学习课程。
        
        请基于以下内容，为章节《{chapter_title}》创建详细的讲解。
        你的回复必须使用以下结构：
        
        # 标题与摘要
        [此章节的标题，以及2-3句话概括主要内容]
        
        # 系统性讲解
        [详细解释本章节的核心概念，提供清晰的定义、示例和应用场景]
        
        # 拓展思考
        [提供额外的思考角度、应用建议或相关领域的连接]
        
        请确保你的解释针对初学者，使用通俗易懂的语言，并保持逻辑清晰。
        
        原始内容:
        {content}
        """
    )


def create_summary_prompt_template() -> ChatPromptTemplate:
    """
    Create a prompt template for generating a course summary.
    
    This template instructs the LLM to generate a comprehensive summary
    of the entire course, based on the original content and chapter summaries.
    
    Returns
    ----
    ChatPromptTemplate
        A prompt template for generating course summaries.
    
    Examples
    -----
    >>> prompt = create_summary_prompt_template()
    >>> prompt.format(content="...", chapters_summary="...")
    """
    return ChatPromptTemplate.from_template(
        """你是一位专业教育工作者，正在为一门课程创建总结。
        
        请基于原始内容和各章节的摘要，创建一个全面的课程总结。
        总结应该概括课程的主要内容、核心概念和学习价值。
        使用简体中文，确保语言通俗易懂，并突出课程的关键要点。
        
        原始内容:
        {content}
        
        章节摘要:
        {chapters_summary}
        """
    )


def generate_toc(content: str, llm: Optional[BaseLanguageModel] = None, temperature: float = 0.0) -> List[str]:
    """
    Generate a table of contents from raw content.
    
    This function takes raw text content and uses an LLM to generate
    a structured table of contents with 1-10 chapter titles.
    
    Parameters
    ----
    content : str
        The raw text content to analyze and create a table of contents for.
    llm : BaseLanguageModel, optional
        The language model to use for generation. If None, the function will use a placeholder
        that should be mocked in tests. For production use, pass a configured LLM instance.
    temperature : float, optional
        The temperature setting for the LLM, affecting randomness in output.
        Default is 0.0 (deterministic output).
    
    Returns
    ----
    List[str]
        A list of chapter titles without numbering.
    
    Examples
    -----
    >>> from langchain_google_genai import ChatGoogleGenerativeAI
    >>> llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.0)
    >>> toc = generate_toc("This is a text about machine learning...", llm=llm)
    >>> print(toc)
    ['Introduction to Machine Learning', 'Supervised Learning Methods', ...]
    """
    # Create the prompt template
    prompt = create_toc_prompt()
    
    # Create the LLM chain - this will be mocked in tests
    # In a real application, a specific LLM model would be used
    chain = LLMChain(
        llm=llm,  # User-provided LLM or None (to be mocked in tests)
        prompt=prompt,
    )
    
    # Invoke the chain with the content
    result = chain.invoke({"content": content})
    
    # Extract and clean up the chapter titles
    chapters = []
    if result.get("text"):
        # Split by newline and process each line
        for line in result["text"].strip().split("\n"):
            # Process each line to clean it up
            clean_line = line.strip()
            
            # Skip empty lines
            if not clean_line:
                continue
            
            # Extract just the chapter title by removing the numbering
            # This pattern matches common numbering patterns at the beginning of a line
            parts = clean_line.split(". ", 1)
            if len(parts) > 1 and parts[0].isdigit():
                clean_line = parts[1].strip()
            
            chapters.append(clean_line)
    
    return chapters


def generate_chapter(chapter_title: str, content: str, llm: Optional[BaseLanguageModel] = None, temperature: float = 0.0) -> ChapterContent:
    """
    Generate a structured explanation for a single chapter.
    
    This function uses an LLM to create a detailed, structured explanation
    for a chapter based on its title and the original content.
    
    Parameters
    ----
    chapter_title : str
        The title of the chapter to explain.
    content : str
        The original raw content to base the explanation on.
    llm : BaseLanguageModel, optional
        The language model to use for generation. If None, the function will use a placeholder
        that should be mocked in tests. For production use, pass a configured LLM instance.
    temperature : float, optional
        The temperature setting for the LLM, affecting randomness in output.
        Default is 0.0 (deterministic output).
    
    Returns
    ----
    ChapterContent
        A structured object containing the chapter's title, summary, explanation, and extension.
    
    Examples
    -----
    >>> from langchain_google_genai import ChatGoogleGenerativeAI
    >>> llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.0)
    >>> chapter = generate_chapter("Machine Learning Basics", "Content about ML...", llm=llm)
    >>> print(chapter.summary)
    'A brief introduction to the fundamental concepts of machine learning...'
    """
    # Create the prompt template
    prompt = create_chapter_prompt_template()
    
    # Create the LLM chain - this will be mocked in tests
    chain = LLMChain(
        llm=llm,  # User-provided LLM or None (to be mocked in tests)
        prompt=prompt,
    )
    
    # Invoke the chain with the chapter title and content
    result = chain.invoke({
        "chapter_title": chapter_title,
        "content": content,
    })
    
    # Parse the result to extract the structured content
    try:
        return parse_chapter_content(chapter_title, result.get("text", ""))
    except Exception as e:
        # Handle parsing errors by creating a basic chapter with an error note
        return ChapterContent(
            title=chapter_title,
            summary=f"Error parsing chapter content: {str(e)}",
            explanation="The LLM response format was unexpected.",
            extension="Please check the LLM configuration and prompt template."
        )


def generate_summary(content: str, chapters: List[ChapterContent], llm: Optional[BaseLanguageModel] = None, temperature: float = 0.0) -> str:
    """
    Generate a comprehensive summary for the entire course.
    
    Parameters
    ----
    content : str
        The original raw content to base the summary on.
    chapters : List[ChapterContent]
        The list of chapter content objects to include in the summary.
    llm : BaseLanguageModel, optional
        The language model to use for generation. If None, the function will use a placeholder
        that should be mocked in tests. For production use, pass a configured LLM instance.
    temperature : float, optional
        The temperature setting for the LLM, affecting randomness in output.
        Default is 0.0 (deterministic output).
    
    Returns
    ----
    str
        A comprehensive summary of the entire course.
    
    Examples
    -----
    >>> from langchain_google_genai import ChatGoogleGenerativeAI
    >>> llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.0)
    >>> chapters = [ChapterContent(title="Chapter 1", summary="Summary 1")]
    >>> summary = generate_summary("Original content", chapters, llm=llm)
    >>> print(summary[:50])
    'This course covers the following key concepts...'
    """
    # Create the prompt template
    prompt = create_summary_prompt_template()
    
    # Prepare the chapter summaries
    chapters_summary = "\n\n".join([
        f"章节 {i+1}: {chapter.title}\n{chapter.summary}"
        for i, chapter in enumerate(chapters)
    ])
    
    # Create the LLM chain
    chain = LLMChain(
        llm=llm,  # User-provided LLM or None (to be mocked in tests)
        prompt=prompt,
    )
    
    # Invoke the chain with the content and chapter summaries
    result = chain.invoke({
        "content": content,
        "chapters_summary": chapters_summary,
    })
    
    return result.get("text", "")


def create_course(content: str, llm: Optional[BaseLanguageModel] = None, temperature: float = 0.0) -> Course:
    """
    Create a complete structured course from raw content.
    
    This function orchestrates the entire course creation process:
    1. Generate a table of contents
    2. Create detailed explanations for each chapter
    3. Generate a comprehensive course summary
    
    Parameters
    ----
    content : str
        The raw content to transform into a course.
    llm : BaseLanguageModel, optional
        The language model to use for generation. If None, the function will use placeholders
        that should be mocked in tests. For production use, pass a configured LLM instance.
    temperature : float, optional
        The temperature setting for the LLM, affecting randomness in output.
        Default is 0.0 (deterministic output).
    
    Returns
    ----
    Course
        A complete course object with all components.
    
    Examples
    -----
    >>> from langchain_google_genai import ChatGoogleGenerativeAI
    >>> llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.0)
    >>> course = create_course("Raw content about a topic...", llm=llm)
    >>> print(f"Generated {len(course.chapters)} chapters")
    """
    # Initialize the course with the original content
    course = Course(content=content)
    
    # Step 1: Generate the table of contents
    chapter_titles = generate_toc(content, llm=llm, temperature=temperature)
    
    # Step 2: Generate content for each chapter
    chapters = []
    for title in chapter_titles:
        chapter = generate_chapter(title, content, llm=llm, temperature=temperature)
        chapters.append(chapter)
    
    course.chapters = chapters
    
    # Step 3: Generate the course summary
    course.summary = generate_summary(content, chapters, llm=llm, temperature=temperature)
    
    return course


def parse_chapter_content(chapter_title: str, text: str) -> ChapterContent:
    """
    Parse the raw text output from the LLM into structured chapter content.
    
    This function extracts the summary, explanation, and extension sections
    from the LLM's response and organizes them into a ChapterContent object.
    
    Parameters
    ----
    chapter_title : str
        The title of the chapter.
    text : str
        The raw text output from the LLM.
    
    Returns
    ----
    ChapterContent
        A structured object containing the chapter's components.
    
    Raises
    -----
    ValueError
        If the text cannot be parsed into the expected sections.
    """
    # Initialize the chapter content with the title
    chapter_content = ChapterContent(title=chapter_title)
    
    # Define section markers
    sections = {
        "summary": ["# 标题与摘要", "# 摘要", "标题与摘要"],
        "explanation": ["# 系统性讲解", "# 讲解", "系统性讲解"],
        "extension": ["# 拓展思考", "# 拓展", "拓展思考"]
    }
    
    # Split the text by section markers
    section_text = {}
    lines = text.split("\n")
    current_section = None
    
    for line in lines:
        stripped_line = line.strip()
        
        # Check if this line is a section marker
        new_section = None
        for section, markers in sections.items():
            if any(stripped_line.startswith(marker) for marker in markers):
                new_section = section
                break
        
        if new_section:
            current_section = new_section
            section_text[current_section] = []
        elif current_section:
            section_text[current_section].append(line)
    
    # Join the lines for each section and add to the chapter content
    if "summary" in section_text and section_text["summary"]:
        chapter_content.summary = "\n".join(section_text["summary"]).strip()
    
    if "explanation" in section_text and section_text["explanation"]:
        chapter_content.explanation = "\n".join(section_text["explanation"]).strip()
    
    if "extension" in section_text and section_text["extension"]:
        chapter_content.extension = "\n".join(section_text["extension"]).strip()
    
    return chapter_content


def configure_gemini_llm(api_key: Optional[str] = None, model_name: str = "gemini-1.5-pro", temperature: float = 0.0) -> BaseLanguageModel:
    """
    Configure and return a Google Gemini model for use with the coursemaker module.
    
    Parameters
    ----
    api_key : str, optional
        The Google API key for accessing Gemini models. If None, will use the 
        GOOGLE_API_KEY environment variable.
    model_name : str, optional
        The name of the Gemini model to use. Default is "gemini-1.5-pro".
    temperature : float, optional
        The temperature setting for generation, affecting randomness in output.
        Default is 0.0 (deterministic output).
    
    Returns
    ----
    BaseLanguageModel
        A configured Gemini language model ready to use with coursemaker functions.
    
    Examples
    -----
    >>> llm = configure_gemini_llm(temperature=0.2)
    >>> course = create_course("Content to transform...", llm=llm)
    
    Notes
    -----
    This function requires the langchain-google-genai package to be installed:
    pip install langchain-google-genai
    """
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError:
        raise ImportError(
            "The langchain-google-genai package is required to use Gemini models. "
            "Please install it with: pip install langchain-google-genai"
        )
    
    return ChatGoogleGenerativeAI(
        google_api_key=api_key,
        model=model_name,
        temperature=temperature
    ) 