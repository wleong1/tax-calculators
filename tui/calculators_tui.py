from rich.text import Text
from textual.app import App, ComposeResult
from textual.await_complete import AwaitComplete
from textual.widgets import Header, Footer, Input, TabPane, TabbedContent, Markdown, Button, Digits
from textual.containers import VerticalScroll, Horizontal
import sys
import os
from textual import events, on

from textual.widgets._tabs import Tab
print(sys.path)
sys.path.append(os.getcwd())
from src import core
from tui import income_tax_gui
from income_tax_gui import Stopwatch


class Calculators(App):
    """
    A textual app to calculate amount of taxes paid.
    """
    CSS_PATH = "calculators_tui.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()
        yield Footer()
        with TabbedContent():
            # core_tab = core.Core()
            # calcs = list(core_tab.GetTools())
            # total_calcs = len(calcs)
            # for idx in range(total_calcs):
            #     curr_calc = calcs[idx]
            #     with TabPane(core_tab.tools[curr_calc].name, id=curr_calc):  # First tab
            #         yield Input(placeholder="Input your salary")
            #         # yield Input(placeholder="Enter your tax code")
            #         yield Button("Calculate", id=curr_calc)
            #         with VerticalScroll(id="results-container"):
            #             yield Markdown(id="results")
            core_tab = core.Core()
            # calc = list(core_tab.GetTools())[0]
            with TabPane(core_tab.tools["income_tax"].name, id="income_tax"):  # First tab
                yield Input(placeholder="Input your salary", id="salary")
                # yield Input(placeholder="Enter your tax code", id="tax-code")
                yield Horizontal(
                    Button("GetName", id="name"),
                    Button("GetCalculationParameters", id="calcparams"),
                    Button("GetAdditionalParameters", id="addparams"),
                    Button("Calculate", id="calc")
                    )
                yield Markdown(id="results")

    @on(Button.Pressed, "#calc") #the "#calc" is to specify that the button is specifically for that id
    def pressed_calc(self) -> None:
        salary_input = self.query_one("#salary", Input)
        results_markdown = self.query_one("#results", Markdown)
        salary_value = salary_input.value.strip()
        core_tab = core.Core()
        if salary_value:
            calculated_result = core_tab.Calculate(tool_name="income_tax", current_salary=int(salary_value), financial_year="2018-19")
            results_markdown.update(str(calculated_result))
        else:
            results_markdown.update("Please enter a valid salary value.")

    @on(Button.Pressed, "#name, #calcparams")
    def pressed_basic_info(self, event: Button.Pressed) -> None:
        results_markdown = self.query_one("#results", Markdown)
        core_tab = core.Core()
        button_id = event.button.id
        if button_id == "name":
            pass
        elif button_id == "calcparams":
            results_markdown.update(str(core_tab.GetCalculationParameters("income_tax")))

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode"""
        self.dark = not self.dark

if __name__ == "__main__":
    app = Calculators()
    app.run()
