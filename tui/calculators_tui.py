from rich.text import Text
from textual.app import App, ComposeResult
from textual.await_complete import AwaitComplete
from textual.widgets import Header, Footer, Input, TabPane, TabbedContent, Markdown, Button, Digits, DataTable, Select
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
import glob


class Calculators(App):
    """
    A textual app to calculate amount of taxes paid.
    """
    CSS_PATH = "calculators_tui.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self) -> None:
        super().__init__()
        self.core_tab = core.Core()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()
        yield Footer()
        with TabbedContent():
            # self.core_tab = core.Core()
            # calcs = list(self.core_tab.GetTools())
            # total_calcs = len(calcs)
            # for idx in range(total_calcs):
            #     curr_calc = calcs[idx]
            #     with TabPane(self.core_tab.tools[curr_calc].name, id=curr_calc):  # First tab
            #         yield Input(placeholder="Input your salary")
            #         # yield Input(placeholder="Enter your tax code")
            #         yield Button("Calculate", id=curr_calc)
            #         with VerticalScroll(id="results-container"):
            #             yield Markdown(id="results")
            # self.core_tab = core.Core()
            # calc = list(self.core_tab.GetTools())[0]
            year_options = [year for year in self.core_tab.GetAdditionalParameters("income_tax", None).keys()]
            year_options.insert(0, "All")
            with TabPane(self.core_tab.tools["income_tax"].name, id="income_tax"):  # First tab
                yield Input(placeholder="Input your salary", id="salary")
                # yield Input(placeholder="Enter your tax code", id="tax-code")
                yield Select.from_values(year_options, allow_blank=False, id="year")
                yield Horizontal(
                    Button("GetName", id="name"),
                    Button("GetCalculationParameters", id="calcparams"),
                    Button("GetAdditionalParameters", id="addparams"),
                    Button("Calculate", id="calc")
                    )
                # yield Markdown(id="results")
                yield DataTable(id="results")
            with TabPane(self.core_tab.tools["national_insurance"].name, id="national_insurance"):  # First tab
                yield Input(placeholder="Input your salary", id="salary")
                # yield Input(placeholder="Enter your tax code", id="tax-code")
                yield Select.from_values(year_options, allow_blank=False, id="year")
                yield Horizontal(
                    Button("GetName", id="name"),
                    Button("GetCalculationParameters", id="calcparams"),
                    Button("GetAdditionalParameters", id="addparams"),
                    Button("Calculate", id="calc")
                    )
                # yield Markdown(id="results")
                yield DataTable(id="results")

    @on(Button.Pressed, "#calc") #the "#calc" is to specify that the button is specifically for that id
    def pressed_calc(self) -> None:
        salary_input = self.query_one("#salary", Input)
        results_markdown = self.query_one("#results", DataTable)
        self.query_one("#results", DataTable).clear(columns=True)
        # results_markdown = self.query_one("#results", Markdown)
        salary_value = salary_input.value.strip()
        chosen_year = self.query_one("#year", Select)
        chosen_year_value = chosen_year.value
        # self.core_tab = core.Core()
        if chosen_year_value != "All":
            try:
                calculated_results = self.core_tab.Calculate(tool_name="income_tax", current_salary=int(salary_value), financial_year=chosen_year_value)
                # results_markdown.update(str(calculated_results))
                # rates = [rate for rate in calculated_results['Annual breakdown']['breakdown'].keys()]
                # first_row = ["Breakdown\Rates"]
                # for rate in rates:
                #     first_row.append(f"{rate*100}%")
                self.format_results(results=calculated_results)
            except ValueError:
                results_markdown.add_columns("Please enter a valid salary value.")
        else:
            results_markdown.add_columns("Please select a year")

    @on(Button.Pressed, '#addparams')
    def pressed_add_info(self) -> None:
        # self.core_tab = core.Core()
        chosen_year = self.query_one("#year", Select)
        chosen_year_value = chosen_year.value
        results_datatable = self.query_one("#results", DataTable)
        self.query_one("#results", DataTable).clear(columns=True)
        rows = []
        if chosen_year_value == "All":
            rows.append(["Year", "Info"])
            for year, info in self.core_tab.GetAdditionalParameters(tool_name="income_tax", financial_year=None).items():
                rows.append([year, str(info)])
        else:
            rows.append(["Info", "Value"])
            for info, value in self.core_tab.GetAdditionalParameters(tool_name="income_tax", financial_year=chosen_year_value).items():
                rows.append([info, value])
        results_datatable.add_columns(*rows[0])
        results_datatable.add_rows(rows[1:])


    @on(Button.Pressed, "#name, #calcparams")
    def pressed_basic_info(self, event: Button.Pressed) -> None:
        results_markdown = self.query_one("#results", DataTable)
        self.query_one('#results', DataTable).clear(columns=True)
        # self.core_tab = core.Core()
        button_id = event.button.id
        if button_id == "name":
            results_markdown.add_column("Calculator Name")
            results_markdown.add_row("Income Tax")
        elif button_id == "calcparams":
            results = self.core_tab.GetCalculationParameters("income_tax")
            first_row = [key for key in results.keys()]
            rows = []
            rows.append([key.capitalize() for key in first_row])
            parameters_required = [results[key] for key in first_row]
            max_number_of_params = max([len(params) for params in parameters_required])
            for idx in range(max_number_of_params):
                curr_row = []
                for params in parameters_required:
                    if idx < len(params):
                        curr_row.append(params[idx])
                    else:
                        curr_row.append("")
                rows.append(curr_row)
                # [1, 1], [1, -], [1, -]
            # results_markdown.update(str(self.core_tab.GetCalculationParameters("income_tax")))
            results_markdown.add_columns(*rows[0])
            results_markdown.add_rows(rows[1:])

    def format_results(self, results) -> None:
        results_datatable = self.query_one("#results", DataTable)
        rows = []
        first_row = []
        rates = [rate for rate in results['Annual breakdown']['breakdown'].keys()]
        first_row = ["Breakdown\Rates"]
        for rate in rates:
            first_row.append(f"{rate*100}%")
        first_row.append("Total")
        rows.append(first_row)
        time_period = [period for period in results.keys()]
        for idx in range(len(time_period)):
            curr_time_period = time_period[idx]
            curr_values = [value for value in results[curr_time_period]['breakdown'].values()]
            # curr_row_data = [f"{curr_time_period}", f"{curr_values[0]}", f"{curr_values[1]}", f"{curr_values[2]}", f"{curr_values[3]}"]
            curr_row_data = [f"{curr_time_period}"]
            for value in curr_values:
                curr_row_data.append(value)
            curr_row_data.append(results[curr_time_period]["total income tax"])
            rows.append(curr_row_data)
        results_datatable.add_columns(*rows[0])
        results_datatable.add_rows(rows[1:])


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode"""
        self.dark = not self.dark

if __name__ == "__main__":
    app = Calculators()
    app.run()
