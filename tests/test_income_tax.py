from src import income_tax

def test_GetName():
    test_income_tax = income_tax.IncomeTax()
    results = test_income_tax.GetName()
    assert results == "Income_Tax"

def test_GetCalculationParameters():
    test_income_tax = income_tax.IncomeTax()
    results = test_income_tax.GetCalculationParameters()
    assert isinstance(results, dict)
    assert results == {"inputs": ["current_salary"], "outputs": ["total_tax"]}

def test_GetAdditionalParameters():
    test_income_tax = income_tax.IncomeTax()
    dummy_data = {
        "personal_allowance": 11000,
        "personal_allowance threshold": 100000,
        "thresholds": [0, 11000, 43000, 150000],
        "rates": [0, 0.2, 0.4, 0.45]
    }
    results = test_income_tax.GetAdditionalParameters()
    assert isinstance(results, dict)
    assert results["2016-17"] == dummy_data

def test_Calculate_under_first_threshold():
    test_income_tax = income_tax.IncomeTax()
    financial_year = "2022-23"
    current_salary = 12570
    calculated_partial_results = {
        'gross income': '12570.00',
        'breakdown': {0: '0.00', 0.2: '0.00', 0.4: '0.00', 0.45: '0.00'},
        'total income tax': '0.00'
        }
    results = test_income_tax.Calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 0.00
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_Calculate_over_first_threshold():
    test_income_tax = income_tax.IncomeTax()
    financial_year = "2022-23"
    current_salary = 29000
    calculated_partial_results = {
        'gross income': '29000.00',
        'breakdown': {0: "0.00", 0.2: "3286.00", 0.4: "0.00", 0.45: "0.00"},
        'total income tax': '3286.00'
        }
    results = test_income_tax.Calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 3286
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_Calculate_over_second_threshold():
    test_income_tax = income_tax.IncomeTax()
    financial_year = "2022-23"
    current_salary = 60000
    calculated_partial_results = {
        'gross income': '60000.00',
        'breakdown': {0: "0.00", 0.2: "7540.00", 0.4: "3892.00", 0.45: "0.00"},
        'total income tax': '11432.00'
        }
    results = test_income_tax.Calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 11432
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_Calculate_over_third_threshold():
    test_income_tax = income_tax.IncomeTax()
    financial_year = "2022-23"
    current_salary = 102000
    calculated_partial_results = {
        'gross income': '102000.00',
        'breakdown': {0: "0.00", 0.2: "7540.00", 0.4: "21092.00", 0.45: "0.00"},
        'total income tax': '28632.00'
        }
    results = test_income_tax.Calculate(current_salary = current_salary, financial_year=financial_year)
    actual_total_tax = 28632
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_Calculate_zero_personal_allowance():
    test_income_tax = income_tax.IncomeTax()
    financial_year = "2021-22"
    current_salary = 200000
    calculated_partial_results = {
        'gross income': '200000.00',
        'breakdown': {0.2: "7540.00", 0.4: "44920.00", 0.45: "22500.00"},
        'total income tax': '74960.00'
        }
    results = test_income_tax.Calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 74960
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_Calculate_wrong_argument_format():
    test_income_tax = income_tax.IncomeTax()
    dummy_financial_year = "2022/23"
    current_salary = 29000
    results = test_income_tax.Calculate(current_salary=current_salary, financial_year=dummy_financial_year)
    assert results == "Year not included in calculator, wrong format provided, \
or incorrect key provided for data. \
Please call GetAdditionalParameters() to find available timeframes and format"

def test_Calculate_salary_error():
    dummy_salary = "90"
    test_income_tax = income_tax.IncomeTax()
    results = test_income_tax.Calculate(current_salary=dummy_salary, financial_year="2022-23")
    assert results == "Please provide a valid salary, in integers"

def test_Calculate_negative_salary():
    dummy_salary = -90
    test_income_tax = income_tax.IncomeTax()
    results = test_income_tax.Calculate(current_salary = dummy_salary, financial_year="2022-23")
    assert results == "Please provide a positive salary"
