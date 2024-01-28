from rich.text import Text
from textual.app import App, ComposeResult
from textual.await_complete import AwaitComplete
from textual.widgets import Header, Footer, Button, TextArea, Static, Tabs, TabPane, TabbedContent, Markdown
from textual.containers import ScrollableContainer
import sys
import os

from textual.widgets._tabs import Tab
print(sys.path)
sys.path.append(os.getcwd())
from src import core


class TimeDisplay(Static):
    """A widget to display elapsed time."""

class Stopwatch(Static):
    """A stopwatch widget."""

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00.00")

class CoreTab(Tabs):
    """Tabs for all available calculators"""
    def __init__(self):
        self.core_module = core.Core(current_salary=29000, tax_code="1257L")

    # def compose(self) -> ComposeResult:
    #     yield


class Calculators(App):
    """
    A textual app to calculate amount of taxes paid.
    """
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()
        yield Footer()
        with TabbedContent("Leto", "Jessica", "Paul"):
            yield Stopwatch()
            yield Markdown("JESS")
            yield Markdown("PAUL")
        # yield ScrollableContainer(Stopwatch(), Stopwatch(), Stopwatch())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode"""
        self.dark = not self.dark

if __name__ == "__main__":
    app = Calculators()
    app.run()