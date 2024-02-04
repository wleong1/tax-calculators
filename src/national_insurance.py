from typing import Union
import os
import sys

sys.path.append(os.getcwd())
from src import national_insurance_info


class NationalInsurance:
    """
    National Insurance calculator for a given salary and financial year.
    """

    def __init__(self) -> None:
        """
        Constructs all the necessary attributes to make the necessary calculations.

        Args:
            None

        Returns:
            None
        """
        self.name: str = "National_Insurance"

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
        data: dict[str, dict] = national_insurance_info.information
        return data

    def Calculate(self, current_salary: int, financial_year: str) -> Union[dict, str]:
        """
        Calculates the amount paid for national insurance in the selected financial year.

        Args:
            financial_year: The year user would like the amount of national insurance to be
            calculated.

        Returns:
            A dictionary of breakdown of the amount paid for each tax bracket and the total amount
            of national insurance paid.
        """
        try:
            financial_year_data: dict = self.GetAdditionalParameters()[financial_year]
        except KeyError:
            return "Year not included in calculator, wrong format provided, or \
incorrect key provided for data. Please call GetAdditionalParameters() \
to find available timeframes and format"

        try:
            if current_salary < 0:
                return "Please provide a positive salary"
            total_tax: float = 0.0
            if "thresholds_annual" in financial_year_data:
                curr_tax: float
                thresholds: list[int] = financial_year_data["thresholds_annual"]
                rates: list[float] = financial_year_data["rates"]
                breakdown: dict[float, float] = {rate: 0.0 for rate in rates}
                idx: int = 1
                length: int = len(thresholds)
                while idx < length:
                    if current_salary - thresholds[idx] >= 0:
                        curr_tax = (thresholds[idx] - thresholds[idx - 1]) * rates[
                            idx - 1
                        ]
                        total_tax += curr_tax
                        breakdown[rates[idx - 1]] = round(curr_tax, 2)
                        idx += 1
                    else:
                        curr_tax = (current_salary - thresholds[idx - 1]) * rates[
                            idx - 1
                        ]
                        total_tax += curr_tax
                        breakdown[rates[idx - 1]] = round(curr_tax, 2)
                        break
                if idx >= length:
                    curr_tax = (current_salary - thresholds[-1]) * rates[-1]
                    total_tax += curr_tax
                    breakdown[rates[idx - 1]] = round(curr_tax, 2)
            else:
                durations: list[str] = list(financial_year_data.keys())
                for duration in durations:
                    curr_tax: float = 0.0
                    thresholds: list[int] = financial_year_data[duration][
                        "thresholds_month"
                    ]
                    rates: list[float] = financial_year_data[duration]["rates"]
                    breakdown: dict[float, float] = {rate: 0.0 for rate in rates}
                    idx: int = 1
                    length: int = len(thresholds)
                    salary: float = current_salary / 12
                    while idx < length:
                        if salary - thresholds[idx] >= 0:
                            curr_tax += (thresholds[idx] - thresholds[idx - 1]) * rates[
                                idx - 1
                            ]
                            # total_tax += curr_tax
                            breakdown[rates[idx - 1]] = round(curr_tax, 2)
                            idx += 1
                        else:
                            curr_tax += (salary - thresholds[idx - 1]) * rates[idx - 1]
                            # total_tax += curr_tax
                            breakdown[rates[idx - 1]] = round(curr_tax, 2)
                            break
                    if idx >= length:
                        curr_tax += (salary - thresholds[-1]) * rates[-1]
                        # total_tax += curr_tax
                        breakdown[rates[idx - 1]] = round(curr_tax, 2)
                    total_tax += int(duration) * curr_tax
            return {
                "Annual breakdown": {
                    "gross income": format(current_salary, ".2f"),
                    "breakdown": breakdown,
                    "total": format(total_tax, ".2f"),
                },
                "Monthly breakdown": {
                    "gross income": format(current_salary / 12, ".2f"),
                    "breakdown": {
                        key: format(value / 12, ".2f")
                        for key, value in breakdown.items()
                    },
                    "total": format(total_tax / 12, ".2f"),
                },
                "Weekly breakdown": {
                    "gross income": format(current_salary / 52, ".2f"),
                    "breakdown": {
                        key: format(value / 52, ".2f")
                        for key, value in breakdown.items()
                    },
                    "total": format(total_tax / 52, ".2f"),
                },
                "Daily breakdown": {
                    "gross income": format(current_salary / 260, ".2f"),
                    "breakdown": {
                        key: format(value / 260, ".2f")
                        for key, value in breakdown.items()
                    },
                    "total": format(total_tax / 260, ".2f"),
                },
            }
        except TypeError:
            return "Please provide a valid salary, in integers"


# a = NationalInsurance()
# print(a.Calculate(200000,"2022-23"))
# print(a.GetAdditionalParameters())
