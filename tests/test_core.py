from src import core

def test_GetTools():
    test_core = core.Core(current_salary=32400, tax_code="1257L")
    results = test_core.GetTools()
    assert isinstance(results, list)
    assert "income_tax" in results
    assert "national_insurance" in results
    assert len(results) == 2

def test_GetCalculationParameters_income_tax():
    test_core = core.Core(current_salary=32400, tax_code="1257L")
    results = test_core.GetCalculationParameters(tool_name="income_tax")
    assert isinstance(results, dict)
    assert results == {"inputs": ["current_salary"], "outputs": ["total_tax"]}

def test_GetCalculationParameters_national_insurance():
    test_core = core.Core(current_salary=32400, tax_code="1257L")
    results = test_core.GetCalculationParameters(tool_name="income_tax")
    assert isinstance(results, dict)
    assert results == {"inputs": ["current_salary"], "outputs": ["total_tax"]}

def test_GetCalculationParameters_key_error():
    test_core = core.Core(current_salary=32400, tax_code="1257L")
    results = test_core.GetCalculationParameters(tool_name="income_tex")
    assert results == "Please provide the correct tool name"

def test_GetAdditionalParameters_income_tax():
    test_core = core.Core(current_salary=32400, tax_code="1257L")
    tool_name = "income_tax"
    financial_year = "2018-19"
    dummy_results = {
        'personal_allowance': 11850,
        'personal_allowance threshold': 100000,
        'thresholds': [0, 11850, 46350, 150000],
        'rates': [0, 0.2, 0.4, 0.45]
        }
    results = test_core.GetAdditionalParameters(tool_name=tool_name, financial_year=financial_year)
    assert isinstance(results, dict)
    assert results == dummy_results

# TODO: Add national insurance, presentation of data for years with multiple rates are not finalised, e.g. 2022-23, 2023-24
def test_GetAdditionalParameters_national_insurance():
    pass

def test_GetAdditionalParameters_key_error():
    test_core = core.Core(current_salary=32400, tax_code="1257L")
    results = test_core.GetAdditionalParameters(tool_name="income_tex", financial_year="2022-23")
    assert results == """
            Incorrect tool name, year not included in calculator or, wrong format provided.
            Call GetTools() to get available tools.
            Correct format for financial_year: "2022-23"   
            """

def test_Calculate_income_tax_under_first_threshold():
    test_core = core.Core(current_salary=12570, tax_code="1257L")
    tool_name = "income_tax"
    financial_year = "2022-23"
    calculated_partial_results = {
        'gross income': '12570.00',
        'breakdown': {0: 0, 0.2: 0, 0.4: 0, 0.45: 0},
        'total income tax': '0.00'
        }
    results = test_core.Calculate(tool_name=tool_name, financial_year=financial_year)
    actual_total_tax = 0.00
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_Calculate_income_tax_over_first_threshold():
    test_core = core.Core(current_salary=29000, tax_code="1257L")
    tool_name = "income_tax"
    financial_year = "2022-23"
    calculated_partial_results = {
        'gross income': '29000.00',
        'breakdown': {0: 0, 0.2: 3286.0, 0.4: 0, 0.45: 0},
        'total income tax': '3286.00'
        }
    results = test_core.Calculate(tool_name=tool_name, financial_year=financial_year)
    actual_total_tax = 3286
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_Calculate_income_tax_over_second_threshold():
    test_core = core.Core(current_salary=60000, tax_code="1257L")
    tool_name = "income_tax"
    financial_year = "2022-23"
    calculated_partial_results = {
        'gross income': '60000.00',
        'breakdown': {0: 0, 0.2: 7540.0, 0.4: 3892.0, 0.45: 0},
        'total income tax': '11432.00'
        }
    results = test_core.Calculate(tool_name=tool_name, financial_year=financial_year)
    actual_total_tax = 11432
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_Calculate_income_tax_over_third_threshold():
    test_core = core.Core(current_salary=102000, tax_code="1257L")
    tool_name = "income_tax"
    financial_year = "2022-23"
    calculated_partial_results = {
        'gross income': '102000.00',
        'breakdown': {0: 0, 0.2: 7540.0, 0.4: 21092.0, 0.45: 0},
        'total income tax': '28632.00'
        }
    results = test_core.Calculate(tool_name=tool_name, financial_year=financial_year)
    actual_total_tax = 28632
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_Calculate_income_tax_zero_personal_allowance():
    test_core = core.Core(current_salary=200000, tax_code="1257L")
    tool_name = "income_tax"
    financial_year = "2021-22"
    calculated_partial_results = {
        'gross income': '200000.00',
        'breakdown': {0.2: 7540.0, 0.4: 44920.0, 0.45: 22500.0},
        'total income tax': '74960.00'
        }
    results = test_core.Calculate(tool_name=tool_name, financial_year=financial_year)
    actual_total_tax = 74960
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_Calculate_income_tax_wrong_argument_format():
    test_core = core.Core(current_salary=29000, tax_code="1257L")
    tool_name = "income_tax"
    dummy_financial_year = "2022/23"
    results = test_core.Calculate(tool_name=tool_name, financial_year=dummy_financial_year)
    assert results == "Year not included in calculator, wrong format provided, \
or incorrect key provided for data. \
Please call GetAdditionalParameters() to find available timeframes and format"

def test_Calculate_income_tax_salary_error():
    dummy_salary = "90"
    test_core = core.Core(current_salary=dummy_salary, tax_code="1257L")
    tool_name = "income_tax"
    results = test_core.Calculate(tool_name=tool_name, financial_year="2022-23")
    assert results == "Please provide a valid salary, in integers"

def test_Calculate_income_tax_negative_salary():
    dummy_salary = -90
    test_core = core.Core(current_salary=dummy_salary, tax_code="1257L")
    tool_name = "income_tax"
    results = test_core.Calculate(tool_name=tool_name, financial_year="2022-23")
    assert results == "Please provide a positive salary"

# TODO: Add national insurance, presentation of data for years with multiple rates are not finalised, e.g. 2022-23, 2023-24
def test_Calculate_national_insurance():
    pass

def test_Calculate_key_error_wrong_tool_name():
    dummy_tool_name = "income_tex"
    test_core = core.Core(current_salary=32400, tax_code="1257L")
    results = test_core.Calculate(tool_name=dummy_tool_name, financial_year="2022-23")
    assert results == "Please provide the correct tool name"

def test_Calculate_key_error_wrong_financial_year():
    dummy_financial_year = "2022-2023"
    test_core = core.Core(current_salary=32400, tax_code="1257L")
    results = test_core.Calculate(tool_name="income_tax", financial_year=dummy_financial_year)
    assert results == "Year not included in calculator, wrong format provided, \
or incorrect key provided for data. \
Please call GetAdditionalParameters() to find available timeframes and format"

# def test_EagerLoad():
#     load_output = test_core.tools
#     assert load_output == []

# def test_LazyLoad():
#     load_output = test_core.tools
#     assert load_output == []
