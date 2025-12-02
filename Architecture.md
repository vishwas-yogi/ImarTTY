# ImarTTY Architecture

ImarTTY is designed as a modular, event-driven terminal emulator. It separates the user interface (TUI) from the core logic (command execution, AI processing) to ensure responsiveness and maintainability.

## 🏗️ High-Level Overview

```mermaid
graph TD
    User[User] --> TUI[Textual TUI (main.py)]
    TUI --> Commander[Commander (utils/commander.py)]
    TUI --> AI[AI Provider (utils/ai.py)]
    TUI --> History[History Manager (utils/history.py)]
    
    Commander --> Shell[System Shell]
    AI --> Gemini[Google Gemini API]
    AI --> Ollama[Ollama Local API]
    
    subgraph "Phase 2: Intelligence Layer"
        Context[Context Manager (utils/context.py)]
        Analyzer[Log Analyzer (utils/log_analyzer.py)]
    end
    
    TUI --> Context
    TUI --> Analyzer
    Context --> AI
    Analyzer --> AI
```

## 🧩 Core Components

### 1. Presentation Layer (`main.py`)
-   **Framework**: Built using [Textual](https://textual.textualize.io/).
-   **Responsibilities**:
    -   Rendering the terminal interface (Input, Output, Header).
    -   Handling user input events.
    -   Displaying streaming output from commands.
    -   Managing application state (current directory, history index).

### 2. Execution Layer (`utils/commander.py`)
-   **Responsibilities**:
    -   Executing shell commands asynchronously using `asyncio.create_subprocess_shell`.
    -   **Rolling Buffer**: Maintains a circular buffer (default 1MB) of the command output to prevent memory exhaustion during long-running processes.
    -   Streaming stdout/stderr back to the TUI in real-time.

### 3. Intelligence Layer (New!)
-   **Context Manager (`utils/context.py`)**:
    -   Scans the current directory to detect project types (Python, Node, Rust, etc.).
    -   Identifies key files (`package.json`, `Dockerfile`) to give the AI "grounding".
-   **Log Analyzer (`utils/log_analyzer.py`)**:
    -   **The Investigator**: Parses log files or command output strings.
    -   **Smart Tail**: Efficiently reads only the last 1MB of large files (>10MB).
    -   **Error Extraction**: Uses heuristics and keywords to identify the root cause of errors.
    -   **Handoff**: Generates structured prompts for other AI agents.

### 4. AI Layer (`utils/ai.py`)
-   **Pattern**: Strategy Pattern.
-   **Interface**: `AIProvider` (abstract base class).
-   **Implementations**:
    -   `GeminiProvider`: Connects to Google's Gemini models.
    -   `OllamaProvider`: Connects to local Ollama instances.
-   **Features**:
    -   `get_command_suggestion`: Translates natural language to shell commands.
    -   `fix_command`: Analyzes exit codes and stderr to suggest fixes.
    -   `analyze_log`: Summarizes log excerpts provided by the Log Analyzer.

### 5. Data Layer
-   **History (`utils/history.py`)**: SQLite database (`history.db`) for persistent command history.
-   **Config (`utils/config.py`)**: YAML-based configuration for themes, API keys, and preferences.

## 🔄 Data Flows

### Command Execution
1.  User types command -> `main.py`.
2.  `main.py` calls `Commander.execute_command`.
3.  `Commander` streams output -> `main.py` (updates UI).
4.  `Commander` stores last 1MB of output in memory.

### AI Assistance (`? query`)
1.  User types `? query` -> `main.py`.
2.  `main.py` calls `ContextManager.get_project_context`.
3.  `main.py` calls `AIProvider.get_command_suggestion(query, context)`.
4.  AI returns shell command -> `main.py` (pre-fills input).

### Log Analysis (`/analyze`)
1.  User runs `/analyze` -> `main.py`.
2.  `main.py` retrieves `last_command_output` from `Commander`.
3.  `main.py` calls `LogAnalyzer.analyze_string`.
4.  `LogAnalyzer` extracts error chunk -> `main.py`.
5.  `main.py` calls `AIProvider.analyze_log(chunk)` for a summary.
6.  UI displays Summary + Copyable Handoff Prompt.
