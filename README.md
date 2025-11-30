# AI Terminal (imarTty)

A modern, AI-powered terminal emulator built with Python and Textual. This project combines a classic command-line interface with the power of Google Gemini to translate natural language queries into executable shell commands.

![AI Terminal Demo](https://via.placeholder.com/800x400?text=AI+Terminal+Demo+Placeholder)

## Features

-   **Standard Terminal Capabilities**: Execute shell commands (`ls`, `grep`, `git`, etc.) with real-time streaming output.
-   **Persistent History**: Commands are saved across sessions. Use **Up/Down** arrows to navigate or type `/history` to view recent commands.
-   **Built-in Navigation**: Supports `cd` to navigate directories and `exit` to close the session.
-   **AI Command Suggestions**: Type `? <query>` to ask the AI for a command (e.g., `? find all large files`).
-   **Modern TUI**: Built on [Textual](https://textual.textualize.io/) for a rich, responsive terminal user interface.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/imarTty.git
    cd imarTty
    ```

2.  **Set up a virtual environment (Recommended):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Key:**
    Create a `.env` file in the root directory and add your Google Gemini API key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

## Configuration

You can customize ImarTTY by creating a `config.yaml` file in the root directory.

```yaml
theme: default
ai_provider: gemini
history_file: ~/.imartty_history.db
```

## Usage

Run the application:

```bash
python main.py
```

### AI Mode
To use the AI features, simply start your command with a question mark `?`:

```bash
? how do I undo the last git commit?
```

The AI will populate the input box with the suggested command (e.g., `git reset --soft HEAD~1`). You can then review it and press **Enter** to execute.

### History
- Press **Up/Down** arrows to cycle through previous commands.
- Type `/history` to see a list of recent commands with their exit status.

## Tech Stack

-   **Python 3.12+**
-   **Textual**: TUI framework.
-   **Google Generative AI**: LLM for command translation.
-   **Asyncio**: For non-blocking command execution and UI updates.
-   **SQLite**: For persistent command history.

