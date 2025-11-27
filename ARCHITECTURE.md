# AI Terminal Architecture & Internals

This document provides a detailed technical overview of the AI Terminal project. It is intended for developers who want to understand the codebase, contribute, or extend its functionality.

## High-Level Architecture

The application is built using the **Model-View-Controller (MVC)** pattern, adapted for the **Textual** framework.

-   **View (UI)**: Defined in `main.py` using Textual widgets (`Input`, `VerticalScroll`, `Static`).
-   **Controller (Logic)**: The `TerminalApp` class in `main.py` handles events (input submission) and orchestrates workers.
-   **Model/Services**:
    -   `utils/commander.py`: Handles shell command execution.
    -   `utils/ai.py`: Handles interaction with the Gemini API.

## Directory Structure

```
imarTty/
├── main.py              # Entry point & UI Logic
├── main.css             # Stylesheet for the TUI
├── utils/
│   ├── commander.py     # Async command runner
│   └── ai.py            # Gemini API client
├── tests/               # Verification scripts
├── .env                 # API Keys (ignored by git)
└── requirements.txt     # Python dependencies
```

## Key Components

### 1. The Event Loop (`main.py`)
The `TerminalApp` class inherits from `textual.app.App`. It runs an async event loop that listens for user input.

-   **`on_input_submitted`**: This is the main trigger. It decides whether to run a standard shell command or an AI query based on the `?` prefix.
-   **`@work` Decorator**: We use Textual's worker API to run long-running tasks (like API calls or shell commands) off the main thread to keep the UI responsive.

### 2. Async Command Execution (`utils/commander.py`)
Executing shell commands without freezing the UI is critical. We use `asyncio.create_subprocess_shell`.

-   **Streaming Output**: We do NOT wait for the command to finish. Instead, we read from `stdout` and `stderr` line-by-line asynchronously and update the UI immediately. This allows running commands like `ping` or long builds.
-   **Built-ins**: `cd` and `exit` are handled specially because they affect the parent process state (the Python app itself), which `subprocess` cannot do.

### 3. AI Integration (`utils/ai.py`)
This module wraps the `google-generativeai` library.

-   **Prompt Engineering**: We use a specific system prompt to ensure the LLM returns *only* the shell command, without markdown formatting or chatter.
-   **Model**: Currently using `gemini-flash-latest` for speed and cost-effectiveness.

## Data Flow

### Standard Command Flow
1.  User types `ls -la` -> `Enter`.
2.  `on_input_submitted` clears input and calls `run_command` (Worker).
3.  `run_command` calls `execute_command`.
4.  `execute_command` spawns subprocess.
5.  As subprocess emits lines, `execute_command` calls the callback.
6.  Callback schedules `append_text` on the **Main Thread** (UI updates must happen on the main thread).
7.  `VerticalScroll` widget updates with new content.

### AI Command Flow
1.  User types `? list files` -> `Enter`.
2.  `on_input_submitted` detects `?`, disables input, and calls `run_ai_query` (Worker).
3.  `run_ai_query` calls `get_command_suggestion`.
4.  `get_command_suggestion` hits Gemini API.
5.  Result is returned to `run_ai_query`.
6.  `run_ai_query` schedules `update_input_with_suggestion` on Main Thread.
7.  Input box is re-enabled and populated with the suggestion.

## Future Roadmap (Phase 3)

-   **PTY Support**: Currently, we use pipes. This means interactive programs (like `vim` or `python` REPL) won't work correctly. Implementing Pseudo-Terminal (PTY) support is the next major technical milestone.
-   **Command History**: Implementing Up/Down arrow history.
-   **Syntax Highlighting**: Using `rich` to highlight command output.
