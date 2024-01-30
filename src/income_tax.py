from typing import Union
import sys
import os
sys.path.append(os.getcwd())
from src import income_tax_info


class IncomeTax:
    """
    Income Tax calculator for a given salary and financial year.
    """
    def __init__(self) -> None:
        """
        Constructs all the necessary attributes to make the necessary calculations.

        Args:
            current_salary: The annual salary to be used for calculations.
            tax_code: The tax code used for calculations.

        Returns:
            None
        """
        self.name: str = "Income_Tax"

    def GetName(self) -> str:
        """
        Returns the name of the calculator.

        Args:
            None

        Returns:
            The name of the calculator in string.
        """
        return self.name

    def GetCalculationParameters(self) -> dict:
        """
        Returns the inputs and outputs of this calculator.

        Args:
            None.

        Returns:
            A dictionary showing the required inputs from user and the outputs user will be given.
        """
        inputs: list[str] = ["current_salary"]
        outputs: list[str] = ["total_tax"]
        return {"inputs": inputs, "outputs": outputs}

    def GetAdditionalParameters(self) -> dict:
        """
        Returns the information, including thresholds and corresponding rates for all available
        financial years.

        Args:
            None.

        Returns:
            A dictionary that shows the information for all tax years.
        """
        data: dict[str, dict] = income_tax_info.information
        return data

    def Calculate(self, current_salary: int, financial_year: str) -> Union[dict, str]:
        """
        Calculates the amount paid for income tax in the selected financial year.

        Args:
            financial_year: The year user would like the amount of income tax to be calculated.

        Returns:
            A dictionary of breakdown of the amount paid for each tax bracket and the total amount
            of income tax paid.
        """
        try:
            financial_year_data: dict = self.GetAdditionalParameters()[financial_year]
        except KeyError:
            return "Year not included in calculator, wrong format provided, \
or incorrect key provided for data. \
Please call GetAdditionalParameters() to find available timeframes and format"

        try:
            if current_salary < 0:
                return "Please provide a positive salary"
            thresholds: list[int] = financial_year_data["thresholds"][:]
            rates: list[float] = financial_year_data["rates"][:]
            # TODO: Include tax codes, for now assumed to be the standard allowance for each year

            # Deduction of personal allowance
            personal_allowance_threshold = financial_year_data["personal_allowance threshold"]
            if (personal_allowance_threshold + thresholds[1]*2 > current_salary >
                personal_allowance_threshold):
                deduction_from_allowance = (current_salary -
                                            personal_allowance_threshold)//2
                for index in range(1, len(thresholds)-1):
                    thresholds[index] -= deduction_from_allowance
            elif current_salary >= personal_allowance_threshold + thresholds[1]*2:
                for index in range(1, len(thresholds)-1):
                    thresholds[index] -= financial_year_data["personal_allowance"]
                thresholds, rates = thresholds[1:], rates[1:]

            # Calculation
            breakdown: dict[float, float] = {rate: 0. for rate in rates}
            total_tax: float = 0.
            idx: int = 1
            length: int = len(thresholds)
            while idx < length:
                if current_salary - thresholds[idx] >= 0:
                    curr_tax = (thresholds[idx] - thresholds[idx - 1]) * rates[idx - 1]
                    total_tax += curr_tax
                    breakdown[rates[idx - 1]] = round(curr_tax, 2)
                    idx += 1
                else:
                    curr_tax = (current_salary - thresholds[idx - 1]) * rates[idx - 1]
                    total_tax += curr_tax
                    breakdown[rates[idx - 1]] = round(curr_tax, 2)
                    break
            if idx >= length:
                curr_tax = (current_salary - thresholds[-1]) * rates[-1]
                total_tax += curr_tax
                breakdown[rates[idx - 1]] = round(curr_tax, 2)
            return {"Annual breakdown":{
                "gross income": format(current_salary, ".2f"),
                "breakdown": {key: format(value, ".2f") for key, value in breakdown.items()},
                "total": format(total_tax, ".2f")
                },
                    "Monthly breakdown":{
                "gross income": format(current_salary/12, ".2f"),
                "breakdown": {key: format(value/12, ".2f") for key, value in breakdown.items()},
                "total": format(total_tax/12, ".2f")
                },
                    "Weekly breakdown":{
                "gross income": format(current_salary/52, ".2f"),
                "breakdown": {key: format(value/52, ".2f") for key, value in breakdown.items()},
                "total": format(total_tax/52, ".2f")
                },
                    "Daily breakdown":{
                "gross income": format(current_salary/260, ".2f"),
                "breakdown": {key: format(value/260, ".2f") for key, value in breakdown.items()},
                "total": format(total_tax/260, ".2f")}}
        except TypeError:
            return "Please provide a valid salary, in integers"
# a = IncomeTax()
# print(a.Calculate(12570.00, "2022-23"))
# results = a.GetAdditionalParameters()
# print(results)
