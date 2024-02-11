import sys
import os
from typing import Union, Any
import click
from prettytable import PrettyTable

sys.path.append(os.getcwd())
from src import core

class Calculators:
    """
    A Command-Line Interface app to calculate the amount of taxes paid for a selected calculator.
    """

    def __init__(self) -> None:
        """
        Constructs all the necessary attributes.

        Args:
            None

        Returns:
            None
        """
        self.core_tab = core.Core()

    def get_tools(self) -> list:
        """
        Gets available calculators.

        Args:
            None

        Returns:
            A list of available calculators.
        """
        return self.core_tab.get_tools()

    def get_calculation_parameters(self, tool_name: str) -> Union[dict, str]:
        """
        Returns the inputs and outputs of the selected calculator.

        Args:
            tool_name: The name of the calculator.

        Returns:
            A dictionary showing the required inputs from user and the outputs user will be given.
        """
        return self.core_tab.get_calculation_parameters(tool_name=tool_name)

    def get_additional_parameters(self, tool_name: str, financial_year: Union[str, None]) -> Union[dict, str]:
        """
        Returns the information, including thresholds and corresponding rates for the selected 
        tax year if there is information for the selected financial year.

        Args:
            tool_name: The name of the calculator.
            financial_year: The year user would like the amount to be calculated.

        Returns:
            A dictionary that shows the information for the selected tax year or all tax years
            if None selected.
            
        """
        return self.core_tab.get_additional_parameters(
            tool_name=tool_name, financial_year=financial_year
            )

    def calculate(self, tool_name: str, current_salary: int, financial_year: Any) -> Union[dict, str]:
        """
        Calculates the amount paid for the selected tool in the selected financial year.

        Args:
            tool_name: The name of the calculator.
            financial_year: The year user would like the amount to be calculated.

        Returns:
            A dictionary of breakdown of the amount paid for each tax bracket and 
            the total amount paid for the selected calculator.
        """
        return self.core_tab.calculate(
            tool_name=tool_name, current_salary=current_salary, financial_year=financial_year
            )

@click.command()
def start_calculator() -> None:
    """
    Starts the calculator app.

    Args:
        None

    Returns:
        None
    """
    calculator_app: Calculators = Calculators()
    while True:
        available_calculators: list = calculator_app.get_tools()
        calculator: str = click.prompt(
            "Please choose a calculator (type 'exit' to quit)\n" + str(available_calculators)
            )

        if calculator == "exit":
            click.echo("Exiting the calculator.")
            break  # Exit the loop if the user types 'exit'

        if calculator in available_calculators:
            calculate(calculator_app, calculator)
        else:
            click.echo("Invalid calculator selected. Please try again.")

def calculate(calculator_app: Calculators, calculator: str) -> None:
    """
    Opens the selected calculator window.

    Args:
        calculator_app: The Calculator class.
        calculator: The name of the calculator.
    
    Returns:
        None
    """
    click.echo(f"\nYou are currently in the {calculator} calculator.")
    while True:
        action: str = click.prompt("""
What would you like to do? (type 'back' to go back)
"name": Shows you the current calculator.
"params": Shows you the inputs and outputs required for this calculator.
"add": Shows you the additional info of this calculator, including thresholds and rates.
"calc": Calculates the total tax required.
                              """)
        table: PrettyTable = PrettyTable()
        if action == "back":
            click.echo("Returning to the calculator selection.")
            break
        if action == "name":
            table.field_names = [f"This is the {calculator} calculator"]
            click.echo(table)
        elif action == "params":
            display_params(calculator_app, calculator, table)
        elif action == "add":
            selected_year: Union[str, None] = click.prompt("""
Please provide the year you would like to see. Leave it blank if you would like to see all years.
""", default="")
            table.clear()
            if not selected_year:
                selected_year = None
            display_additional_params(calculator_app, calculator, table, selected_year)
        elif action == "calc":
            table.clear()
            salary: str = click.prompt("Please provide your salary")
            financial_year: str = click.prompt("Please provide the financial year")
            display_results(calculator_app, calculator, table, salary, financial_year)

def display_params(calculator_app: Calculators, calculator: str, table: PrettyTable) -> None:
    """
    Displays the parameters required for the calculator.

    Args:
        calculator_app: The Calculator class.
        calculator: The name of the calculator.
        table: The table in which the output will be populated.
    
    Returns:
        None

    """
    basic_info: Union[dict, str] = calculator_app.get_calculation_parameters(tool_name=calculator)
    assert isinstance(basic_info, dict)
    table.clear()
    headers: list = list(basic_info.keys())
    table.field_names = headers
    parameters_required: list = [basic_info[key] for key in headers]
    max_number_of_params: int = max([len(params) for params in parameters_required])
    for idx in range(max_number_of_params):
        curr_row: list = []
        for params in parameters_required:
            if idx < len(params):
                curr_row.append(params[idx])
            else:
                curr_row.append("")
        table.add_row(curr_row)
    click.echo(table)

def display_additional_params(calculator_app, calculator, table, selected_year) -> None:
    """
    Displays the information, including thresholds and corresponding 
    rates for all available financial years.

    Args:
        calculator_app: The Calculator class.
        calculator: The name of the calculator.
        table: The table in which the output will be populated.
        selected_year: The year user would like to see the additional information in,
                        leaving it blank will display all years' information.
    
    Returns:
        None

    """
    additional_info: Union[dict, str] = calculator_app.get_additional_parameters(
        tool_name=calculator, financial_year=selected_year
        )
    if isinstance(additional_info, dict):
        rows: list = []
        if selected_year is None:
            table.field_names = ["Year", "Info"]
            for year, info in additional_info.items():
                rows.append([year, str(info)])
        else:
            table.field_names = ["Info", "Value"]
            for info, value in additional_info.items():
                rows.append([info, value])
        table.add_rows(rows)
        click.echo(f"Additional info:\n{table}")
    else:
        table.field_names = [additional_info]
        click.echo(table)

def display_results(calculator_app, calculator, table, salary, financial_year) -> None:
    """
    Calculates and displays the results.

    Args:
        calculator_app: The Calculator class.
        calculator: The name of the calculator.
        table: The table in which the output will be populated.
        salary: The salary in which the tax will be calculated on.
        financial_year: The year user would like the amount to be calculated.
    
    Returns:
        None

    """
    try:
        results: Union[dict, str] = calculator_app.calculate(
            tool_name=calculator, current_salary=int(salary), financial_year=financial_year
            )
    except ValueError:
        results = calculator_app.calculate(
            tool_name=calculator, current_salary=salary, financial_year=financial_year
            )
    if isinstance(results, str):
        table.field_names = [results]
        click.echo(f"\nCalculation results:\n{table}")
    else:
        rows: list = []
        rates: list = list(results['Annual breakdown']['breakdown'].keys())
        headers: list = ["Breakdown\Rates"] # pylint: disable=W1401
        for rate in rates:
            headers.append(f"{rate*100}%")
        headers.append("Total")
        table.field_names = headers
        time_period: list = list(results.keys())
        for _, period in enumerate(time_period):
            curr_time_period: str = period
            curr_values: list = list(results[curr_time_period]['breakdown'].values())
            curr_row_data: list = [f"{curr_time_period}"]
            for value in curr_values:
                curr_row_data.append(value)
            curr_row_data.append(results[curr_time_period]["total"])
            rows.append(curr_row_data)
        table.add_rows(rows)
        click.echo(f"""
Calculation results:
Salary: {salary}, Financial year: {financial_year}                           
{table}""")

if __name__ == "__main__":
    start_calculator()
