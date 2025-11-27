from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static
from textual.containers import VerticalScroll
from textual import work
from utils.commander import execute_command
from utils.ai import get_command_suggestion
import os

class TerminalApp(App):
    """A simple AI-powered terminal app."""

    CSS_PATH = "main.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(id="output-container")
        yield Input(placeholder="Type your command here... (Start with ? for AI)", id="command-input")
        yield Footer()

    def on_mount(self) -> None:
        """Called when app starts."""
        self.title = "AI Terminal (Phase 2)"
        self.query_one(Input).focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value
        input_widget = self.query_one("#command-input", Input)
        output_container = self.query_one("#output-container", VerticalScroll)

        if not command.strip():
            return

        # Check for AI trigger
        if command.startswith("?"):
            query = command[1:].strip()
            if query:
                input_widget.value = "Thinking..."
                input_widget.disabled = True
                self.run_ai_query(query)
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
        suggestion = get_command_suggestion(query)
        self.call_from_thread(self.update_input_with_suggestion, suggestion)

    def update_input_with_suggestion(self, command: str) -> None:
        """Updates the input widget with the AI's suggestion."""
        input_widget = self.query_one("#command-input", Input)
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

        await execute_command(command, update_output)

    def append_text(self, widget: Static, text: str, container: VerticalScroll) -> None:
        """Appends text to the widget and scrolls."""
        widget.user_text += text
        widget.update(widget.user_text)
        container.scroll_end(animate=False)

if __name__ == "__main__":
    app = TerminalApp()
    app.run()
