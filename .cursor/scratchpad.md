# [TASK] Implement "Cascade" Mode for Course Generation

This mode generates chapters sequentially, where the content of each new chapter is informed by the content of all previously generated chapters. This mode disables parallel processing.

## 1. Analysis & Task Breakdown (Planner)
- [x] **Task 1: Core Logic Implementation.** In `src/geminiteacher/coursemaker.py`, create a new function `create_course_cascade` that generates chapters sequentially. The `content` for generating chapter `N` should be a combination of the original content and the generated content from chapters `1` to `N-1`.

- [x] **Task 2: CLI Integration.** In `src/geminiteacher/app/generate_course.py`, add a `--mode` argument to the CLI. The options should be `sequential`, `parallel`, and `cascade`. The `main` function should call the appropriate `create_course*` function based on this argument.

- [x] **Task 3: GUI Integration.** In `src/geminiteacher/gui/main_window.py`, add a UI element (e.g., a dropdown menu or radio buttons) to allow the user to select the generation mode (`Sequential`, `Parallel`, `Cascade`). The `Worker` thread should then invoke the corresponding function based on the user's selection.

- [x] **Task 4: Update Documentation.** Update `README.md` and any other relevant documentation to explain the new "Cascade" mode and how to use it via the CLI and GUI.

## 2. Executor Log & Status
- **DONE**: Task 1 - Core Logic Implementation (create_course_cascade function)
- **DONE**: Task 2 - CLI Integration (added mode parameter to create_course_with_progressive_save and main functions)
- **DONE**: Task 3 - GUI Integration (added mode dropdown and updated UI logic)
- **DONE**: Task 4 - Update Documentation (updated README.md and docs/usage.md with cascade mode information)

## 3. Reviewer's Audit & Feedback (Reviewer Only)
*N/A*

## 4. Lessons & Discoveries
- The cascade mode provides a more coherent narrative flow between chapters by building upon previously generated content.
- Adding a new generation mode required changes in multiple parts of the codebase: core logic, CLI, GUI, and documentation.
- Using a dropdown in the GUI for mode selection is more intuitive than checkboxes, as the modes are mutually exclusive.
- Proper testing of the cascade mode is important to ensure that each chapter correctly builds upon the content of previous chapters. 