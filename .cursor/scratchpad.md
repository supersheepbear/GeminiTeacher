# Planner's Scratchpad

## Background and Motivation

The user wants to improve the performance of the course generation process by introducing parallel processing. The current implementation generates chapters sequentially, which is time-consuming as it waits for each API call to complete before starting the next.

The goal is to use a multiprocessing pool to generate chapters concurrently, while respecting API rate limits and ensuring the final output is correctly ordered. The implementation should also be robust, with retries for failed API calls, and adhere to the project's coding standards.

## Key Challenges and Analysis

1.  **Parallel Execution**: The core logic needs to be refactored to allow individual chapters to be generated in separate processes. The `concurrent.futures.ProcessPoolExecutor` is a suitable tool for this.
2.  **Maintaining Order**: Chapter content must be assembled and saved in the correct sequence (Chapter 1, Chapter 2, etc.), even though the generation will happen in parallel and may finish out of order. `ProcessPoolExecutor.map` is a good choice here as it returns results in the order that tasks were submitted.
3.  **Rate Limiting**: Sending a large number of API requests simultaneously can trigger rate limits. A mechanism to introduce a small, random delay between submitting tasks to the process pool is required. Researching the specific rate limits for `gemini-1.5-flash` will be necessary to determine a safe delay strategy.
4.  **Error Handling**: API calls can fail due to network issues, timeouts, or empty responses. A retry mechanism must be implemented within the chapter generation function to handle these transient errors gracefully.
5.  **Testability**: The introduction of multiprocessing and `time.sleep` makes testing more complex. Tests will require significant mocking to remain fast and isolated unit tests, as per the repository's rules. We will need to mock the `ProcessPoolExecutor`, the delay function, and the API call itself.

## High-level Task Breakdown

1.  **Research Rate Limits**: Investigate the API rate limits for `gemini-2.5-flash` to inform the delay strategy.
2.  **Refactor for Parallelism**: Isolate the logic for generating a single chapter into a dedicated, self-contained function. This function will be the target for the multiprocessing pool.
3.  **Implement Multiprocessing Orchestrator**:
    *   Create a main function that prepares a list of tasks (e.g., a list of chapter titles or prompts).
    *   Use `concurrent.futures.ProcessPoolExecutor` to manage a pool of worker processes.
    *   Implement a loop that submits chapter generation tasks to the pool, including a small, random delay (`time.sleep`) between each submission.
4.  **Implement Robustness Features**:
    *   Inside the chapter generation function, wrap the API call in a loop or use a decorator to implement retry logic for timeouts or empty responses.
5.  **Manage Output**:
    *   Collect the results from the completed tasks.
    *   Ensure the results are sorted or handled in the correct chapter order before writing them to their respective markdown files.
6.  **Update Unit Tests**:
    *   Write new unit tests for the multiprocessing orchestrator.
    *   Mock `ProcessPoolExecutor`, `time.sleep`, and the chapter generation function.
    *   Verify that tasks are submitted with delays and that results are handled correctly.
    *   Add tests for the retry mechanism.

## Project Status Board

- [x] **Task 1: Research `gemini-2.5-flash` (Paid Tier) rate limits.**
- [ ] **Task 2: Refactor single chapter generation into a callable function.**
- [ ] **Task 3: Implement the `ProcessPoolExecutor` to manage parallel execution.**
- [ ] **Task 4: Add a random delay between task submissions to avoid rate limiting.**
- [ ] **Task 5: Implement retry logic for API calls within the chapter generation function.**
- [ ] **Task 6: Ensure results are collected and saved in the correct order.**
- [ ] **Task 7: Create comprehensive unit tests with appropriate mocking.**

## Executor's Feedback or Assistance Requests
*(To be filled by the Executor)*

## Reviewer's Audit & Feedback
*(To be filled by the Reviewer)*

## Lessons

- **`gemini-2.5-flash` Rate Limits (Tier 1 Paid User)**: The official documentation specifies the following limits:
    - **Requests Per Minute (RPM): 1,000**
    - Tokens Per Minute (TPM): 1,000,000
    - Requests Per Day (RPD): 10,000
- **Strategy**: The 1,000 RPM limit is very generous. The primary concern is not hitting the API with a large number of requests all at once. A small, randomized delay (e.g., between 0.1 and 0.5 seconds) between submitting tasks to the pool is a good practice to ensure smooth processing and avoid potential issues, even when technically under the RPM limit. 