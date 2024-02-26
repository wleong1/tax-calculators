"""This module provides the necessary code for text user interface."""
import sys
import os
from typing import Union, Any
from textual.app import App, ComposeResult
from textual.widgets import (
    Header,
    Footer,
    Input,
    TabPane,
    TabbedContent,
    Button,
    DataTable,
    Select,
)
from textual.containers import Horizontal
from textual import on

sys.path.append(os.getcwd())  # pylint: disable=C0413
from src import core


class Calculators(App):
    """
    A textual app to calculate amount of taxes paid for a selected calculator.
    """

    CSS_PATH = "calculators_tui.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self) -> None:
        """
        Constructs all the necessary attributes.

        Args:
            None

        Returns:
            None
        """
        super().__init__()
        self.core_tab: core.Core = core.Core()

    def compose(self) -> ComposeResult:
        """
        Create child widgets for the app.

        Args:
            None

        Returns:
            ComposeResult
        """
        yield Header()
        yield Footer()
        with TabbedContent():
            calcs: list = list(self.core_tab.get_tools())
            for calc in calcs:
                with TabPane(self.core_tab.tools[calc].name, id=calc):  # First tab
                    all_info = self.core_tab.get_additional_parameters(
                        calc, financial_year=None
                    )
                    assert isinstance(all_info, dict)
                    year_options: list = list(all_info.keys())
                    year_options.insert(0, "All")
                    yield Input(placeholder="Input your salary", id=calc + "_salary")
                    # yield Input(placeholder="Enter your tax code", id="tax-code")
                    yield Select.from_values(
                        year_options, allow_blank=False, id=calc + "_year", value="All"
                    )
                    yield Horizontal(
                        Button("GetName", id="name"),
                        Button("get_calculation_parameters", id="calcparams"),
                        Button("get_additional_parameters", id="addparams"),
                        Button("Calculate", id="calc"),
                    )
                    yield DataTable(id=calc + "_results")

    @on(
        Button.Pressed, "#calc"
    )  # the "#calc" is to specify that the button is specifically for that id # pylint: disable=line-too-long
    def pressed_calc(self) -> None:
        """
        Calculates the total tax paid and returns a breakdown for the selected calculator.

        Args:
            None

        Returns:
            None
        """
        tab_name: str = self.query_one(TabbedContent).active
        salary_input: Input = self.query_one(f"#{tab_name}_salary", Input)
        results_markdown: DataTable = self.query_one(f"#{tab_name}_results", DataTable)
        self.query_one(f"#{tab_name}_results", DataTable).clear(columns=True)
        salary_value: str = salary_input.value.strip()
        chosen_year: Select = self.query_one(f"#{tab_name}_year", Select)
        chosen_year_value: Any = chosen_year.value
        if chosen_year_value != "All":
            try:
                calculated_results: Union[dict, str] = self.core_tab.calculate(
                    tool_name=tab_name,
                    current_salary=int(salary_value),
                    financial_year=chosen_year_value,
                )
                self.format_results(results=calculated_results, tool_name=tab_name)
            except ValueError:
                results_markdown.add_columns("Please enter a valid salary value.")
        else:
            results_markdown.add_columns("Please select a year")

    @on(Button.Pressed, "#addparams")
    def pressed_add_info(self) -> None:
        """
        Returns the information, including thresholds and corresponding rates for all available
        financial years.

        Args:
            None

        Returns:
            None
        """
        tab_name: str = self.query_one(TabbedContent).active
        chosen_year: Select = self.query_one(f"#{tab_name}_year", Select)
        chosen_year_value: Any = chosen_year.value
        results_datatable: DataTable = self.query_one(f"#{tab_name}_results", DataTable)
        self.query_one(f"#{tab_name}_results", DataTable).clear(columns=True)
        rows: list = []
        if chosen_year_value == "All":
            rows.append(["Year", "Info"])
            all_info = self.core_tab.get_additional_parameters(
                tool_name=tab_name, financial_year=None
            )
            assert isinstance(all_info, dict)
            for year, info in all_info.items():
                rows.append([year, str(info)])
        else:
            rows.append(["Info", "Value"])
            all_info = self.core_tab.get_additional_parameters(
                tool_name=tab_name, financial_year=chosen_year_value
            )
            assert isinstance(all_info, dict)
            for info, value in all_info.items():
                rows.append([info, value])
        results_datatable.add_columns(*rows[0])
        results_datatable.add_rows(rows[1:])

    @on(Button.Pressed, "#name, #calcparams")
    def pressed_basic_info(self, event: Button.Pressed) -> None:
        """
        Returns some basic information of the selected calculator, including name of calculator,
        and expected inputs and outputs.

        Args:
            None

        Returns:
            None
        """
        tab_name: str = self.query_one(TabbedContent).active
        results_datatable: DataTable = self.query_one(f"#{tab_name}_results", DataTable)
        self.query_one(f"#{tab_name}_results", DataTable).clear(columns=True)
        assert isinstance(event.button.id, str)
        button_id: str = event.button.id
        if button_id == "name":
            results_datatable.add_column("Calculator Name")
            results_datatable.add_row(self.core_tab.tools[tab_name].get_name())
        elif button_id == "calcparams":
            results: Union[dict, str] = self.core_tab.get_calculation_parameters(
                tool_name=tab_name
            )
            assert isinstance(results, dict)
            first_row: list = list(results.keys())
            rows: list = []
            rows.append([key.capitalize() for key in first_row])
            parameters_required: list = [results[key] for key in first_row]
            max_number_of_params: int = max(
                [len(params) for params in parameters_required]
            )  # pylint: disable=R1728
            for idx in range(max_number_of_params):
                curr_row: list = []
                for params in parameters_required:
                    if idx < len(params):
                        curr_row.append(params[idx])
                    else:
                        curr_row.append("")
                rows.append(curr_row)
            results_datatable.add_columns(*rows[0])
            results_datatable.add_rows(rows[1:])

    def format_results(self, results, tool_name) -> None:
        """
        Formats the calculated results for them to be displayed in a table.

        Args:
            results: Calculated results.
            tool_name: Name of the calculator.

        Returns:
            None
        """
        results_datatable: DataTable = self.query_one(
            f"#{tool_name}_results", DataTable
        )
        rows: list = []
        rates: list = list(results["Annual breakdown"]["breakdown"].keys())
        first_row: list = ["Breakdown\Rates"]  # pylint: disable=W1401
        for rate in rates:
            first_row.append(f"{rate*100}%")
        first_row.append("Total")
        rows.append(first_row)
        time_period: list = list(results.keys())
        for _, period in enumerate(time_period):
            curr_time_period: str = period
            curr_values: list = list(results[curr_time_period]["breakdown"].values())
            curr_row_data: list = [f"{curr_time_period}"]
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
