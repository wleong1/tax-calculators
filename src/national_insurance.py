import os, sys
sys.path.append(os.getcwd())
from src import national_insurance_info

class NationalInsurance:

    def __init__(self, current_salary) -> None:
        self.salary = current_salary
        self.name = "NationalInsurance"

    def GetName(self) -> str:
        return self.name
    
    def GetCalculationParameters(self) -> list:
        inputs: list = ["current_salary"]
        outputs: list = ["total_tax"]
        return {"inputs": inputs, "outputs": outputs}
    
    def GetAdditionalParameters(self) -> dict:
        data = national_insurance_info.information
        return data
    
    def Calculate(self, financial_year: str) -> int:
        try:
            financial_year_data = self.GetAdditionalParameters()[financial_year]
        except KeyError:
            return "Year not included in calculator, wrong fromat provided, or incorrect key provided for data. Please call GetAdditionalParameters to find available timeframes and format"
        
        try:
            if self.salary < 0:
                return "Please provide a positive salary"
            if "thresholds_annual" in financial_year_data:
                thresholds, rates = financial_year_data["thresholds_annual"], financial_year_data["rates"]
                breakdown = {rate: 0 for rate in rates}
                curr_tax = 0
                idx = 1
                length = len(thresholds)
                total_tax = 0
                while idx < length:
                    if self.salary - thresholds[idx] >= 0:
                        curr_tax = (thresholds[idx] - thresholds[idx - 1]) * rates[idx - 1]
                        total_tax += curr_tax
                        breakdown[rates[idx - 1]] = curr_tax
                        idx += 1
                    else:
                        curr_tax = (self.salary - thresholds[idx - 1]) * rates[idx - 1]
                        total_tax += curr_tax
                        breakdown[rates[idx - 1]] = curr_tax
                        break
                if idx >= length:
                    curr_tax = (self.salary - thresholds[-1]) * rates[-1]
                    total_tax += curr_tax
                    breakdown[rates[idx - 1]] = curr_tax
            else:
                durations = list(financial_year_data.keys())
                total_tax = 0
                for duration in durations:
                    thresholds, rates = financial_year_data[duration]["thresholds_month"], financial_year_data[duration]["rates"]
                    breakdown = {rate: 0 for rate in rates}
                    curr_tax = 0
                    idx = 1
                    length = len(thresholds)
                    salary = self.salary / 12
                    while idx < length:
                        if salary - thresholds[idx] >= 0:
                            curr_tax += (thresholds[idx] - thresholds[idx - 1]) * rates[idx - 1]
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
            return {"Annual breakdown":{"gross income": format(self.salary, ".2f"), "breakdown": breakdown, "total NI": format(total_tax, ".2f")},
                    "Monthly breakdown":{"gross income": format(self.salary/12, ".2f"), "breakdown": {key: format(value/12, ".2f") for key, value in breakdown.items()}, "total NI": format(total_tax/12, ".2f")},
                    "Weekly breakdown":{"gross income": format(self.salary/52, ".2f"), "breakdown": {key: format(value/52, ".2f") for key, value in breakdown.items()}, "total NI": format(total_tax/52, ".2f")},
                    "Daily breakdown":{"gross income": format(self.salary/260, ".2f"), "breakdown": {key: format(value/260, ".2f") for key, value in breakdown.items()}, "total NI": format(total_tax/260, ".2f")}}
        except TypeError:
            return "Please provide a valid salary, in integers"
a = NationalInsurance(5000)
print(a.Calculate("2018-19"))
# print(a.GetAdditionalParameters())