# AI Terminal (imarTty)

A modern, AI-powered terminal emulator built with Python and Textual. This project combines a classic command-line interface with the power of Google Gemini to translate natural language queries into executable shell commands.

![AI Terminal Demo](https://via.placeholder.com/800x400?text=AI+Terminal+Demo+Placeholder)


```bash
imartty
# OR if running from source
python main.py
```

### AI Mode
To use the AI features, simply start your command with a question mark `?`:

```bash
? how do I undo the last git commit?
```

The AI will populate the input box with the suggested command (e.g., `git reset --soft HEAD~1`). You can then review it and press **Enter** to execute.

### AI Shortcuts
- **Ctrl+F**: **Fix Error**. If a command fails, press this to ask AI for a fix.
- **Ctrl+E**: **Explain Command**. Press this to get an explanation of the last executed command.
- **AI Provider**: `utils/ai.py` handles communication with Gemini or Ollama.

## 🗺️ Roadmap (Phase 3 Ideas)

- **Git Integration**: `? commit` to automatically generate commit messages based on `git diff`.
- **Interactive TUI**: A dedicated "Analysis Mode" screen with syntax highlighting and chat.
- **Config UI**: Edit settings and API keys directly within the application.
- **Plugin System**: Allow custom Python scripts to extend ImarTTY's capabilities.
- **Smart Suggestions**: `? run tests` will suggest `pytest` for Python or `npm test` for Node, based on your actual files.

### 🛡️ Robust & Scalable
- **Smart Output Handling**: Automatically manages memory by keeping a rolling buffer of the last 1MB of command output. Run `docker compose` or long builds without fear.
- **Large File Support**: The `/analyze` command intelligently reads the tail of massive log files (>100MB), ensuring you get the most recent errors without crashing.

### 🕵️ Log Analysis & The Investigator (New!)
Debug faster by letting ImarTTY analyze your logs and command outputs.
- **`/analyze <file>`**: Scans a log file, finds the root cause error, and generates a summary.

### History
- Press **Up/Down** arrows to cycle through previous commands.
- Type `/history` to see a list of recent commands with their exit status.

## Development

### Running Tests
```bash
pytest
```

### Logging
Logs are written to `imartty.log` in JSON format for easy parsing and debugging.

## Tech Stack

-   **Python 3.12+**
-   **Textual**: TUI framework.
-   **Google Generative AI / Ollama**: LLM providers.
-   **Asyncio**: For non-blocking command execution and UI updates.
-   **SQLite**: For persistent command history.

