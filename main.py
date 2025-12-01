from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from tui.widgets import HistoryInput
from textual.containers import VerticalScroll
from textual import work
from textual.binding import Binding
from utils.commander import execute_command
from utils.ai import get_provider
from utils.history import HistoryManager
from utils.history import HistoryManager
from utils.config import ConfigManager
from utils.logger import setup_logging, get_logger
import os

logger = get_logger("main")

class TerminalApp(App):
    """A simple AI-powered terminal app."""

    CSS_PATH = "main.tcss"
    
    BINDINGS = [
        Binding("ctrl+f", "fix_last_error", "Fix Error"),
        Binding("ctrl+e", "explain_last_command", "Explain Command"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(id="output-container")
        yield HistoryInput(placeholder="Type your command here... (Start with ? for AI)", id="command-input")
        yield Footer()

    def on_mount(self) -> None:
        """Called when app starts."""
        setup_logging()
        logger.info("Application started")
        self.title = "AI Terminal (Phase 2)"
        
        # Initialize managers
        self.config_manager = ConfigManager()
        self.history_manager = HistoryManager(
            db_path=self.config_manager.get("history_file")
        )
        
        # Initialize AI Provider
        self.ai_provider = get_provider(self.config_manager.get("ai_provider", "gemini"))
        
        self.last_command = ""
        self.last_error = ""
        self.last_exit_code = 0
        
        # Load initial history
        self.update_history_widget()
        
        self.query_one(HistoryInput).focus()

    def update_history_widget(self):
        """Load recent commands into the input widget."""
        recent = self.history_manager.get_recent(limit=50)
        # get_recent returns (id, command, timestamp, exit_code)
        # We just want the command strings
        commands = [row[1] for row in recent]
        self.query_one(HistoryInput).set_history(commands)

    async def on_input_submitted(self, event: HistoryInput.Submitted) -> None:
        command = event.value
        input_widget = self.query_one("#command-input", HistoryInput)
        output_container = self.query_one("#output-container", VerticalScroll)

        if not command.strip():
            return

        logger.info(f"Input submitted: {command}")

        # Check for AI trigger
        if command.startswith("?"):
            query = command[1:].strip()
            if query:
                input_widget.value = "Thinking..."
                input_widget.disabled = True
                self.run_ai_query(query)
            return

        # Handle /history command
        if command.strip() == "/history":
            input_widget.value = ""
            self.show_history()
            return

        # Clear input
        input_widget.value = ""

        cwd = os.getcwd()
        prompt = f"\n[bold green]{cwd}[/bold green] $ [bold]{command}[/bold]\n"
        output_container.mount(Static(prompt, classes="output-line"))
        
        # Scroll to end
        output_container.scroll_end(animate=False)

        # Run command
        self.run_command(command)

    @work(exclusive=True, thread=True)
    def run_ai_query(self, query: str) -> None:
        """Runs the AI query in a background thread worker."""
        suggestion = self.ai_provider.get_command_suggestion(query)
        self.call_from_thread(self.update_input_with_suggestion, suggestion)

    def update_input_with_suggestion(self, command: str) -> None:
        """Updates the input widget with the AI's suggestion."""
        input_widget = self.query_one("#command-input", HistoryInput)
        input_widget.disabled = False
        input_widget.value = command
        input_widget.focus()

    @work(exclusive=True)
    async def run_command(self, command: str) -> None:
        """Runs the command in an async worker (main thread)."""
        output_container = self.query_one("#output-container", VerticalScroll)
        
        output_widget = Static("", classes="output-line")
        output_widget.user_text = ""  # Custom attribute to track content
        await output_container.mount(output_widget)
        
        async def update_output(text: str) -> None:
            self.append_text(output_widget, text, output_container)

        exit_code, full_output = await execute_command(command, update_output)
        
        # Save to history
        self.history_manager.add_entry(command, exit_code, full_output)
        self.update_history_widget()
        
        logger.info(f"Command executed: {command}, Exit Code: {exit_code}")
        
        self.last_command = command
        self.last_exit_code = exit_code
        self.last_error = full_output if exit_code != 0 else ""

        if exit_code != 0:
            error_msg = f"Command failed with exit code {exit_code}"
            output_container.mount(Static(error_msg, classes="error-widget"))
            output_container.scroll_end(animate=False)

    def append_text(self, widget: Static, text: str, container: VerticalScroll) -> None:
        """Appends text to the widget and scrolls."""
        widget.user_text += text
        widget.update(widget.user_text)
        container.scroll_end(animate=False)

    def show_history(self):
        """Display history in the output."""
        output_container = self.query_one("#output-container", VerticalScroll)
        recent = self.history_manager.get_recent(limit=20)
        
        history_text = "[bold blue]Recent History:[/bold blue]\n"
        for row in reversed(recent):
            # row: (id, command, timestamp, exit_code)
            status = "[green]✓[/green]" if row[3] == 0 else "[red]✗[/red]"
            history_text += f"{status} {row[1]}\n"
            
        output_container.mount(Static(history_text, classes="output-line"))
        output_container.scroll_end(animate=False)

    @work(exclusive=True, thread=True)
    def action_fix_last_error(self) -> None:
        """Ask AI to fix the last error."""
        if self.last_exit_code == 0 or not self.last_error:
            self.notify("No recent error to fix.")
            return

        self.notify("Asking AI for a fix...")
        suggestion = self.ai_provider.fix_command(self.last_command, self.last_error)
        self.call_from_thread(self.update_input_with_suggestion, suggestion)

    @work(exclusive=True, thread=True)
    def action_explain_last_command(self) -> None:
        """Ask AI to explain the last command."""
        if not self.last_command:
            self.notify("No command run yet.")
            return

        self.notify("Asking AI for explanation...")
        explanation = self.ai_provider.explain_command(self.last_command)
        
        self.call_from_thread(self.show_explanation, explanation)

    def show_explanation(self, explanation: str) -> None:
        """Show explanation in the output."""
        output_container = self.query_one("#output-container", VerticalScroll)
        panel = f"[bold yellow]AI Explanation:[/bold yellow]\n{explanation}\n"
        output_container.mount(Static(panel, classes="output-line"))
        output_container.scroll_end(animate=False)

if __name__ == "__main__":
    app = TerminalApp()
    app.run()
