from typing import Union
import sys
import os
from src import income_tax_info
sys.path.append(os.getcwd())

class IncomeTax:
    def __init__(self, current_salary: int, tax_code: str) -> None:
        self.salary: int = current_salary
        self.tax_code: str = tax_code
        self.name: str = "IncomeTax"

    def GetName(self) -> str:
        return self.name

    def GetCalculationParameters(self) -> dict:
        inputs: list[str] = ["current_salary"]
        outputs: list[str] = ["total_tax"]
        return {"inputs": inputs, "outputs": outputs}

    def GetAdditionalParameters(self) -> dict:
        data: dict[str, dict] = income_tax_info.information
        return data

    def Calculate(self, financial_year: str) -> Union[dict, str]:
        try:
            financial_year_data: dict = self.GetAdditionalParameters()[financial_year]
        except KeyError:
            return "Year not included in calculator, wrong format provided, \
or incorrect key provided for data. \
Please call GetAdditionalParameters() to find available timeframes and format"

        try:
            if self.salary < 0:
                return "Please provide a positive salary"
            thresholds: list[int] = financial_year_data["thresholds"][:]
            rates: list[float] = financial_year_data["rates"][:]
            # TODO: Include tax codes, for now assumed to be the standard allowance for each year
            if (self.salary > financial_year_data["personal_allowance threshold"] and
            self.salary < financial_year_data["personal_allowance threshold"] + thresholds[1] * 2):
                deduction_from_allowance = (self.salary - financial_year_data["personal_allowance threshold"]) // 2
                for idx in range(1, len(thresholds)-1):
                    thresholds[idx] -= deduction_from_allowance
            elif self.salary >= financial_year_data["personal_allowance threshold"] + thresholds[1] * 2:
                for idx in range(1, len(thresholds)-1):
                    thresholds[idx] -= financial_year_data["personal_allowance"]
                thresholds, rates = thresholds[1:], rates[1:]
            breakdown: dict[float, float] = {rate: 0. for rate in rates}
            total_tax: float = 0.
            idx: int = 1
            length: int = len(thresholds)
            while idx < length:
                if self.salary - thresholds[idx] >= 0:
                    curr_tax = (thresholds[idx] - thresholds[idx - 1]) * rates[idx - 1]
                    total_tax += curr_tax
                    breakdown[rates[idx - 1]] = round(curr_tax, 2)
                    idx += 1
                else:
                    curr_tax = (self.salary - thresholds[idx - 1]) * rates[idx - 1]
                    total_tax += curr_tax
                    breakdown[rates[idx - 1]] = round(curr_tax, 2)
                    break
            if idx >= length:
                curr_tax = (self.salary - thresholds[-1]) * rates[-1]
                total_tax += curr_tax
                breakdown[rates[idx - 1]] = round(curr_tax, 2)
            return {"Annual breakdown":{
                "gross income": format(self.salary, ".2f"),
                "breakdown": breakdown,
                "total income tax": format(total_tax, ".2f")
                },
                    "Monthly breakdown":{
                "gross income": format(self.salary/12, ".2f"),
                "breakdown": {key: format(value/12, ".2f") for key, value in breakdown.items()},
                "total income tax": format(total_tax/12, ".2f")
                },
                    "Weekly breakdown":{
                "gross income": format(self.salary/52, ".2f"),
                "breakdown": {key: format(value/52, ".2f") for key, value in breakdown.items()},
                "total income tax": format(total_tax/52, ".2f")
                },
                    "Daily breakdown":{
                "gross income": format(self.salary/260, ".2f"),
                "breakdown": {key: format(value/260, ".2f") for key, value in breakdown.items()},
                "total income tax": format(total_tax/260, ".2f")}}
        except TypeError:
            return "Please provide a valid salary, in integers"
a = IncomeTax(102000, "1257L")
print(a.Calculate("2022-23"))
