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
            calcs = list(self.core_tab.GetTools())
            for calc in calcs:
                with TabPane(self.core_tab.tools[calc].name, id=calc):  # First tab
                    year_options = [year for year in self.core_tab.GetAdditionalParameters(calc, None).keys()]
                    year_options.insert(0, "All")
                    yield Input(placeholder="Input your salary", id=calc+"_salary")
                    # yield Input(placeholder="Enter your tax code", id="tax-code")
                    yield Select.from_values(year_options, allow_blank=False, id=calc+"_year")
                    yield Horizontal(
                        Button("GetName", id="name"),
                        Button("GetCalculationParameters", id="calcparams"),
                        Button("GetAdditionalParameters", id="addparams"),
                        Button("Calculate", id="calc")
                        )
                    yield DataTable(id=calc+"_results")

    @on(Button.Pressed, "#calc") #the "#calc" is to specify that the button is specifically for that id
    def pressed_calc(self) -> None:
        tab_name = self.query_one(TabbedContent).active
        salary_input = self.query_one(f"#{tab_name}_salary", Input)
        results_markdown = self.query_one(f"#{tab_name}_results", DataTable)
        self.query_one(f"#{tab_name}_results", DataTable).clear(columns=True)
        salary_value = salary_input.value.strip()
        chosen_year = self.query_one(f"#{tab_name}_year", Select)
        chosen_year_value = chosen_year.value
        if chosen_year_value != "All":
            try:
                calculated_results = self.core_tab.Calculate(tool_name=tab_name, current_salary=int(salary_value), financial_year=chosen_year_value)
                self.format_results(results=calculated_results, tool_name=tab_name)
            except ValueError:
                results_markdown.add_columns("Please enter a valid salary value.")
        else:
            results_markdown.add_columns("Please select a year")

    @on(Button.Pressed, '#addparams')
    def pressed_add_info(self) -> None:
        tab_name = self.query_one(TabbedContent).active
        chosen_year = self.query_one(f"#{tab_name}_year", Select)
        chosen_year_value = chosen_year.value
        results_datatable = self.query_one(f"#{tab_name}_results", DataTable)
        self.query_one(f"#{tab_name}_results", DataTable).clear(columns=True)
        rows = []
        if chosen_year_value == "All":
            rows.append(["Year", "Info"])
            for year, info in self.core_tab.GetAdditionalParameters(tool_name=tab_name, financial_year=None).items():
                rows.append([year, str(info)])
        else:
            rows.append(["Info", "Value"])
            for info, value in self.core_tab.GetAdditionalParameters(tool_name=tab_name, financial_year=chosen_year_value).items():
                rows.append([info, value])
        results_datatable.add_columns(*rows[0])
        results_datatable.add_rows(rows[1:])


    @on(Button.Pressed, "#name, #calcparams")
    def pressed_basic_info(self, event: Button.Pressed) -> None:
        tab_name = self.query_one(TabbedContent).active
        results_markdown = self.query_one(f"#{tab_name}_results", DataTable)
        self.query_one(f"#{tab_name}_results", DataTable).clear(columns=True)
        button_id = event.button.id
        if button_id == "name":
            results_markdown.add_column("Calculator Name")
            results_markdown.add_row(self.core_tab.tools[tab_name].GetName())
        elif button_id == "calcparams":
            results = self.core_tab.GetCalculationParameters(tool_name=tab_name)
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
            results_markdown.add_columns(*rows[0])
            results_markdown.add_rows(rows[1:])

    def format_results(self, results, tool_name) -> None:
        results_datatable = self.query_one(f"#{tool_name}_results", DataTable)
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
            curr_row_data = [f"{curr_time_period}"]
            for value in curr_values:
                curr_row_data.append(value)
            curr_row_data.append(results[curr_time_period]["total"])
            rows.append(curr_row_data)
        results_datatable.add_columns(*rows[0])
        results_datatable.add_rows(rows[1:])


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode"""
        self.dark = not self.dark

if __name__ == "__main__":
    app = Calculators()
    app.run()
