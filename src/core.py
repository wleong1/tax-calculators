from typing import Union
import sys
import os
from src import income_tax, national_insurance
sys.path.append(os.getcwd())

class Core:
    def __init__(self, current_salary: int, tax_code: str) -> None:
        self.tools: dict = {}
        income_tax_calc: object = income_tax.IncomeTax(current_salary, tax_code)
        national_insurance_calc: object = national_insurance.NationalInsurance(current_salary)
        self.tools["income_tax"]: object = income_tax_calc
        self.tools["national_insurance"]: object = national_insurance_calc

    def GetTools(self) -> list:
        # try:
        return list(self.tools.keys())
        # except TypeError:
        # return "Please check if the number of arguments provided are correct. \n Arguments for this method: 0"

    def GetCalculationParameters(self, tool_name: str) -> Union[dict, str]:
        try:
            curr_tool: object = self.tools[tool_name]
            return curr_tool.GetCalculationParameters()
        except KeyError:
            return "Please provide the correct tool name"
        # except TypeError:
        #     return "Please check if the number of arguments provided are correct. \n Arguments for this method: 1"

    def GetAdditionalParameters(self, tool_name: str, financial_year: str) -> Union[dict, str]:
        try:
            data: dict[str, dict] = self.tools[tool_name].GetAdditionalParameters()
            return data[financial_year]
        except KeyError:
            return """
            Incorrect tool name, year not included in calculator or, wrong format provided.
            Call GetTools() to get available tools.
            Correct format for financial_year: "2022-23"   
            """
        # except TypeError:
        # return "Please check if the number of arguments provided are correct. \n Arguments for this method: 2"

    def Calculate(self, tool_name: str, financial_year: str) -> Union[dict, str]:
        try:
            return self.tools[tool_name].Calculate(financial_year)
        except KeyError:
            return "Please provide the correct tool name"
        # except TypeError:
        # return "Please check if the number of arguments provided are correct. \n Arguments for this method: 2"

    # def EagerLoad(self) -> None:
    #     pass

    # def LazyLoad(self, calculator: __module__) -> None:
    #     pass
        # curr_dir = os.path.dirname(os.path.realpath(__file__))
        # print(curr_dir)
        # try:
        #     for (dirpath, dirnames, filenames) in os.walk(curr_dir):
        #         modules = set(filenames)
        #         if calculator + ".py" in modules:
        #             importlib.import_module(calculator)
        #             break
                # from curr_dir import income_tax
                # print(type(income_tax))
                # print("a")
        # except ModuleNotFoundError as e:
        #     print("No such calculator")

        # except ImportError as e:
        #     print("No such calculator")

# a = Core(20000, "1257L")
# print(a.GetTools())
# print(a.GetCalculationParameters("national_insurance"))
# print(a.GetAdditionalParameters("national_insurane", "2023-245"))
# print(a.Calculate("national_insurance", "2022-232"))