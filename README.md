# AI Terminal (imarTty)

A modern, AI-powered terminal emulator built with Python and Textual. This project combines a classic command-line interface with the power of Google Gemini (and local LLMs) to translate natural language queries into executable shell commands, debug errors, and explain complex operations.

![AI Terminal Demo](https://via.placeholder.com/800x400?text=AI+Terminal+Demo+Placeholder)

## 🚀 Features

### 🧠 Core AI Capabilities
-   **Natural Language to Shell**: Type `? find all large files` and get `find . -type f -size +100M`.
-   **Explain Command**: Press `Ctrl+E` to get a plain-English breakdown of what the last command did.
-   **Fix Error**: Press `Ctrl+F` when a command fails; AI will analyze the error and suggest a fix.
-   **Smart Suggestions**: `? run tests` will suggest `pytest` for Python or `npm test` for Node, based on your actual files.

### 🕵️ Log Analysis & The Investigator (New!)
Debug faster by letting ImarTTY analyze your logs and command outputs.
-   **`/analyze <file>`**: Scans a log file, finds the root cause error, and generates a summary.
-   **`/analyze` (No args)**: Instantly analyzes the output of the *last command you ran*.
-   **Agent Handoff**: Generates a "Golden Prompt" with the error context that you can **Copy to Clipboard** and paste into your favorite coding agent.

### 🛡️ Robust & Scalable
-   **Smart Output Handling**: Automatically manages memory by keeping a rolling buffer of the last 1MB of command output. Run `docker compose` or long builds without fear.
-   **Large File Support**: The `/analyze` command intelligently reads the tail of massive log files (>100MB), ensuring you get the most recent errors without crashing.

### 💻 Standard Terminal Features
-   **Persistent History**: Commands are saved across sessions. Use **Up/Down** arrows to navigate or type `/history` to view recent commands.
-   **Built-in Navigation**: Supports `cd` to navigate directories and `exit` to close the session.
-   **Modern TUI**: Built on [Textual](https://textual.textualize.io/) for a rich, responsive terminal user interface.

## 🛠️ Installation

You can install ImarTTY directly from the source:

```bash
git clone https://github.com/vishwas-yogi/ImarTTY.git
cd ImarTTY
```

**Set up Virtual Environment**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ⚙️ Configuration

1.  **API Keys**: Create a `.env` file for your API keys:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

2.  **App Config**: Customize the app via `config.yaml`:
    ```yaml
    theme: default
    ai_provider: gemini  # Options: gemini, ollama
    history_file: ~/.imartty_history.db
    ```

### Local LLM (Ollama)
To use a local model like Llama 3:
1.  Install [Ollama](https://ollama.com/).
2.  Run `ollama run llama3`.
3.  Set `ai_provider: ollama` in `config.yaml`.

## 🎮 Usage

Start the terminal:
```bash
python main.py
```

### Commands
| Command | Description |
| :--- | :--- |
| `? <query>` | Ask AI for a shell command (e.g., `? list all pdfs`) |
| `/analyze` | Analyze the output of the last command for errors |
| `/analyze <file>` | Analyze a specific log file |
| `/history` | Show command history |
| `Ctrl+E` | Explain the last command |
| `Ctrl+F` | Fix the last failed command |
| `Ctrl+C` | Quit |

## 🏗️ Architecture

ImarTTY is built with a modular architecture:
-   **TUI**: Built with [Textual](https://textual.textualize.io/).
-   **Context Engine**: `utils/context.py` scans the filesystem to understand project structure.
-   **Log Analyzer**: `utils/log_analyzer.py` parses logs and extracts error stack traces.
-   **AI Provider**: `utils/ai.py` handles communication with Gemini or Ollama.
