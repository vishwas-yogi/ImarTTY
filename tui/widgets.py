from textual.widgets import Input
from textual.binding import Binding
from textual.events import Key

class HistoryInput(Input):
    """Input widget with history navigation."""
    
    BINDINGS = [
        Binding("up", "history_up", "History Up"),
        Binding("down", "history_down", "History Down"),
        Binding("ctrl+f", "fix_last_error", "Fix Error"),
        Binding("ctrl+e", "explain_last_command", "Explain Command"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = []
        self.history_index = -1
        self.current_input = ""

    def set_history(self, history: list[str]):
        """Set the history list (newest first)."""
        self.history = history
        self.history_index = -1

    def action_history_up(self):
        """Navigate back in history."""
        if not self.history:
            return

        if self.history_index == -1:
            self.current_input = self.value
        
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.value = self.history[self.history_index]
            self.cursor_position = len(self.value)

    def action_history_down(self):
        """Navigate forward in history."""
        if self.history_index > 0:
            self.history_index -= 1
            self.value = self.history[self.history_index]
            self.cursor_position = len(self.value)
        elif self.history_index == 0:
            self.history_index = -1
            self.value = self.current_input
            self.cursor_position = len(self.value)
