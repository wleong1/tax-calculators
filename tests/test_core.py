from src import core, income_tax, national_insurance  

def test_GetTools():
    test_core = core.Core(current_salary=32400, tax_code="1257L")
    results = test_core.GetTools()
    assert type(results) == list
    assert "income_tax" in results
    assert "national_insurance" in results
    assert len(results) == 2

def test_GetCalculationParameters_income_tax():
    test_core = core.Core(current_salary=32400, tax_code="1257L")
    results = test_core.GetCalculationParameters(tool_name="income_tax")
    assert type(results) == dict
    assert results == {"inputs": ["current_salary"], "outputs": ["total_tax"]}
    
def test_GetCalculationParameters_national_insurance():
    test_core = core.Core(current_salary=32400, tax_code="1257L")
    results = test_core.GetCalculationParameters(tool_name="income_tax")
    assert type(results) == dict
    assert results == {"inputs": ["current_salary"], "outputs": ["total_tax"]}

def test_GetAdditionalParameters_income_tax():
    test_core = core.Core(current_salary=32400, tax_code="1257L")
    tool_name = "income_tax"
    financial_year = "2018-19"
    dummy_results = {'personal_allowance': 11850, 'personal_allowance threshold': 100000, 'thresholds': [0, 11850, 46350, 150000], 'rates': [0, 0.2, 0.4, 0.45]}
    results = test_core.GetAdditionalParameters(tool_name=tool_name, financial_year=financial_year)
    assert type(results) == dict
    assert results == dummy_results

# TODO: Add national insurance
def test_GetAdditionalParameters_national_insurance():
    pass

def test_Calculate_income_tax():
    test_core = core.Core(current_salary=29000, tax_code="1257L")
    tool_name = "income_tax"
    financial_year = "2022-23"
    dummy_partial_results = dummy_partial_results = {'gross income': '29000.00', 'breakdown': {0: 0, 0.2: 3286.0, 0.4: 0, 0.45: 0}, 'total income tax': '3286.00'}
    results = test_core.Calculate(tool_name=tool_name, financial_year=financial_year)
    assert type(results) == dict
    assert dummy_partial_results == results["Annual breakdown"]

# TODO: Add national insurance
def test_Calculate_national_insurance():
    pass

# def test_EagerLoad():
#     load_output = test_core.tools
#     assert load_output == []

# def test_LazyLoad():
#     load_output = test_core.tools
#     assert load_output == []
