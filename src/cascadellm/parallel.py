"""Parallel processing utilities for the CascadeLLM coursemaker module."""
import random
import time
import logging
from concurrent.futures import ProcessPoolExecutor
from typing import List, Optional, Callable, Any, TypeVar, Dict

from langchain_core.language_models import BaseLanguageModel

from cascadellm.coursemaker import ChapterContent, generate_chapter

# Type variable for generic return type
T = TypeVar('T')

def generate_chapter_with_retry(
    chapter_title: str, 
    content: str, 
    llm: Optional[BaseLanguageModel] = None,
    temperature: float = 0.0,
    custom_prompt: Optional[str] = None,
    max_retries: int = 3,
    retry_delay: float = 1.0
) -> ChapterContent:
    """
    Generate a chapter with retry logic for handling API failures.
    
    This function wraps the generate_chapter function with retry logic to handle
    transient API errors, timeouts, or empty responses.
    
    Parameters
    ----------
    chapter_title : str
        The title of the chapter to generate.
    content : str
        The raw content to use for generating the chapter.
    llm : Optional[BaseLanguageModel], optional
        The language model to use. If None, a default model will be configured.
    temperature : float, optional
        The temperature setting for generation. Default is 0.0.
    custom_prompt : Optional[str], optional
        Custom instructions to append to the chapter generation prompt.
    max_retries : int, optional
        Maximum number of retry attempts. Default is 3.
    retry_delay : float, optional
        Base delay between retries in seconds. Default is 1.0.
        
    Returns
    -------
    ChapterContent
        The generated chapter content.
        
    Notes
    -----
    This function implements an exponential backoff strategy for retries,
    with each retry attempt waiting longer than the previous one.
    """
    logger = logging.getLogger("cascadellm.parallel")
    
    for attempt in range(max_retries + 1):
        try:
            chapter = generate_chapter(
                chapter_title=chapter_title,
                content=content,
                llm=llm,
                temperature=temperature,
                custom_prompt=custom_prompt
            )
            
            # Check if we got a valid response (non-empty explanation)
            if chapter.explanation.strip():
                return chapter
            else:
                raise ValueError("Empty chapter explanation received")
                
        except Exception as e:
            if attempt < max_retries:
                # Calculate backoff with jitter
                backoff = retry_delay * (2 ** attempt) + random.uniform(0, 1)
                logger.warning(
                    f"Chapter generation failed for '{chapter_title}' "
                    f"(attempt {attempt + 1}/{max_retries + 1}): {str(e)}. "
                    f"Retrying in {backoff:.2f}s..."
                )
                time.sleep(backoff)
            else:
                logger.error(
                    f"All retry attempts failed for chapter '{chapter_title}'. "
                    f"Last error: {str(e)}"
                )
                # Return a basic chapter with error information
                return ChapterContent(
                    title=chapter_title,
                    summary="Error: Failed to generate chapter content after multiple attempts.",
                    explanation=f"The chapter generation process encountered repeated errors: {str(e)}",
                    extension="Please try regenerating this chapter or check your API configuration."
                )


def parallel_map_with_delay(
    func: Callable[..., T],
    items: List[Any],
    max_workers: Optional[int] = None,
    delay_range: tuple = (0.1, 0.5),
    **kwargs
) -> List[T]:
    """
    Execute a function on multiple items in parallel with a delay between submissions.
    
    This function uses ProcessPoolExecutor to parallelize the execution of a function
    across multiple items, while introducing a random delay between task submissions
    to avoid overwhelming external APIs with simultaneous requests.
    
    Parameters
    ----------
    func : Callable[..., T]
        The function to execute in parallel.
    items : List[Any]
        The list of items to process.
    max_workers : Optional[int], optional
        Maximum number of worker processes. If None, uses the default
        (typically the number of CPU cores).
    delay_range : tuple, optional
        Range (min, max) in seconds for the random delay between task submissions.
        Default is (0.1, 0.5).
    **kwargs
        Additional keyword arguments to pass to the function.
        
    Returns
    -------
    List[T]
        List of results in the same order as the input items.
        
    Examples
    --------
    >>> def process_item(item, factor=1):
    ...     return item * factor
    >>> items = [1, 2, 3, 4, 5]
    >>> results = parallel_map_with_delay(process_item, items, factor=2)
    >>> print(results)
    [2, 4, 6, 8, 10]
    """
    logger = logging.getLogger("cascadellm.parallel")
    results = []
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks with a delay between submissions
        futures = []
        for item in items:
            # Add a small random delay to avoid overwhelming the API
            delay = random.uniform(delay_range[0], delay_range[1])
            logger.debug(f"Submitting task with delay: {delay:.2f}s")
            time.sleep(delay)
            
            # Submit the task to the process pool
            future = executor.submit(func, item, **kwargs)
            futures.append(future)
        
        # Collect results in the original order
        for future in futures:
            results.append(future.result())
    
    return results


def parallel_generate_chapters(
    chapter_titles: List[str],
    content: str,
    llm: Optional[BaseLanguageModel] = None,
    temperature: float = 0.0,
    custom_prompt: Optional[str] = None,
    max_workers: Optional[int] = None,
    delay_range: tuple = (0.1, 0.5),
    max_retries: int = 3
) -> List[ChapterContent]:
    """
    Generate multiple chapters in parallel with retry logic and rate limiting.
    
    This function orchestrates the parallel generation of multiple chapters,
    handling API rate limits and retrying failed requests.
    
    Parameters
    ----------
    chapter_titles : List[str]
        List of chapter titles to generate.
    content : str
        The raw content to use for generating chapters.
    llm : Optional[BaseLanguageModel], optional
        The language model to use. If None, a default model will be configured.
    temperature : float, optional
        The temperature setting for generation. Default is 0.0.
    custom_prompt : Optional[str], optional
        Custom instructions to append to the chapter generation prompt.
    max_workers : Optional[int], optional
        Maximum number of worker processes. If None, uses the default.
    delay_range : tuple, optional
        Range (min, max) in seconds for the random delay between task submissions.
        Default is (0.1, 0.5).
    max_retries : int, optional
        Maximum number of retry attempts per chapter. Default is 3.
        
    Returns
    -------
    List[ChapterContent]
        List of generated chapter contents in the same order as the input titles.
    """
    logger = logging.getLogger("cascadellm.parallel")
    logger.info(f"Starting parallel generation of {len(chapter_titles)} chapters")
    
    # Prepare the kwargs to pass to generate_chapter_with_retry
    kwargs = {
        "content": content,
        "llm": llm,
        "temperature": temperature,
        "custom_prompt": custom_prompt,
        "max_retries": max_retries
    }
    
    # Generate chapters in parallel with delay between submissions
    chapters = parallel_map_with_delay(
        generate_chapter_with_retry,
        chapter_titles,
        max_workers=max_workers,
        delay_range=delay_range,
        **kwargs
    )
    
    logger.info(f"Completed parallel generation of {len(chapters)} chapters")
    return chapters 