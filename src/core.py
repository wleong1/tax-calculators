from typing import Union, Any
import sys
import os
sys.path.append(os.getcwd())
from src import income_tax, national_insurance


class Core:
    """
    A class to display available calculators and calculate annual amount paid for a specific tax.
    """
    def __init__(self) -> None:
        """
        Constructs all the necessary attributes to make the necessary calculations and eager
        loads all calculators.

        Args:
            None

        Returns:
            None
        """
        self.tools: dict = {}
        income_tax_calc: object = income_tax.IncomeTax()
        national_insurance_calc: object = national_insurance.NationalInsurance()
        self.tools["income_tax"] = income_tax_calc
        self.tools["national_insurance"] = national_insurance_calc

    def GetTools(self) -> list:
        """
        Returns a list of available calculators.

        Args:
            None

        Returns:
            The list of available calculators.
        """
        # try:
        return list(self.tools.keys())
        # except TypeError:
        # return "Please check if the number of arguments provided are correct. \n Arguments for this method: 0" # pylint: disable=C0301

    def GetCalculationParameters(self, tool_name: str) -> Union[dict, str]:
        """
        Returns the inputs and outputs of the selected calculator.

        Args:
            tool_name: The name of the calculator.

        Returns:
            A dictionary showing the required inputs from user and the outputs user will be given.
        """
        try:
            curr_tool: Union[income_tax.IncomeTax, national_insurance.NationalInsurance] = self.tools[tool_name]
            return curr_tool.GetCalculationParameters()
        except KeyError:
            return "Please provide the correct tool name"
        # except TypeError:
        #     return "Please check if the number of arguments provided are correct. \n Arguments for this method: 1" # pylint: disable=C0301

    def GetAdditionalParameters(self, tool_name: str, financial_year: Union[str, None]) -> Union[dict, str]:
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
        try:
            data: dict[str, dict] = self.tools[tool_name].GetAdditionalParameters()
            if financial_year:
                return data[financial_year]
            return data
        except KeyError:
            return """
            Incorrect tool name, year not included in calculator or, wrong format provided.
            Call GetTools() to get available tools.
            Correct format for financial_year: "2022-23"   
            """
        # except TypeError:
        # return "Please check if the number of arguments provided are correct. \n Arguments for this method: 2" # pylint: disable=C0301

    def Calculate(self, tool_name: str, current_salary: int, financial_year: Any) -> Union[dict, str]:
        """
        Calculates the amount paid for the selected tool in the selected financial year.

        Args:
            tool_name: The name of the calculator.
            financial_year: The year user would like the amount to be calculated.

        Returns:
            A dictionary of breakdown of the amount paid for each tax bracket and 
            the total amount paid for the selected calculator.
        """
        try:
            return self.tools[tool_name].Calculate(current_salary, financial_year)
        except KeyError:
            return "Please provide the correct tool name"
        # except TypeError:
        # return "Please check if the number of arguments provided are correct. \n Arguments for this method: 2" # pylint: disable=C0301

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

# a = Core()
# print(a.GetTools())
# print(a.GetCalculationParameters("national_insurance"))
# print(a.GetAdditionalParameters("national_insurance", None))
# print(a.Calculate("national_insurance", "2022-232"))
