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

You can install ImarTTY directly from the source:

```bash
git clone https://github.com/yourusername/imarTty.git
cd imarTty
pip install .
```

Alternatively, for development:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file for your API keys:
```env
GEMINI_API_KEY=your_api_key_here
```

Customize the app via `config.yaml`:

```yaml
theme: default
ai_provider: gemini  # Options: gemini, ollama
history_file: ~/.imartty_history.db
```

### Local LLM (Ollama)
To use a local model like Llama 3:
1. Install [Ollama](https://ollama.com/).
2. Run `ollama run llama3`.
3. Set `ai_provider: ollama` in `config.yaml`.

## Usage

Run the application:

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

