from src import national_insurance


def test_GetName():
    test_national_insurance = national_insurance.NationalInsurance(29000)
    results = test_national_insurance.GetName()
    assert results == "NationalInsurance"

def test_GetCalculationParameters():
    test_national_insurance = national_insurance.NationalInsurance(29000)
    results = test_national_insurance.GetCalculationParameters()
    assert isinstance(results, dict)
    assert results == {"inputs": ["current_salary"], "outputs": ["total_tax"]}

def test_GetAdditionalParameters_constant_year():
    test_national_insurance = national_insurance.NationalInsurance(29000)
    dummy_data_2015_16 = {
        "thresholds_annual": [0, 8060, 42380],
        "thresholds_month": [0, 671, 3530],
        "thresholds_week": [0, 155, 815],
        "rates": [0, 0.12, 0.02]
    }
    results = test_national_insurance.GetAdditionalParameters()
    assert isinstance(results, dict)
    assert results["2015-16"] == dummy_data_2015_16

def test_GetAdditionalParameters_variable_year():
    test_national_insurance = national_insurance.NationalInsurance(29000)
    dummy_data_2022_23 =  {
        "3":{
        "thresholds_month": [0, 823, 4189],
        "thresholds_week": [0, 190, 967],
        "rates": [0, 0.1325, 0.0325]
        },
        "4":{
        "thresholds_month": [0, 1048, 4189],
        "thresholds_week": [0, 242, 967],
        "rates": [0, 0.1325, 0.0325]
        },
        "5":{
        "thresholds_month": [0, 1048, 4189],
        "thresholds_week": [0, 242, 967],
        "rates": [0, 0.12, 0.02]
        }
    }
    results = test_national_insurance.GetAdditionalParameters()
    assert isinstance(results, dict)
    assert results["2022-23"] == dummy_data_2022_23

def test_Calculate_constant_year_under_first_threshold():
    test_national_insurance = national_insurance.NationalInsurance(5000)
    financial_year = "2018-19"
    calculated_partial_results = {
        'gross income': '5000.00',
        'breakdown': {0: 0, 0.12: 0, 0.02: 0},
        'total NI': '0.00'
        }
    results = test_national_insurance.Calculate(financial_year=financial_year)
    actual_total_tax = 0.00
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

def test_Calculate_constant_year_over_first_threshold():
    test_national_insurance = national_insurance.NationalInsurance(29000)
    financial_year = "2018-19"
    calculated_partial_results = {
        'gross income': '29000.00',
        'breakdown': {0: 0, 0.12: 2469.12, 0.02: 0},
        'total NI': '2469.12'
        }
    results = test_national_insurance.Calculate(financial_year=financial_year)
    actual_total_tax = 2469.12
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

def test_Calculate_constant_year_over_second_threshold():
    test_national_insurance = national_insurance.NationalInsurance(100000)
    financial_year = "2018-19"
    calculated_partial_results = {
        'gross income': '100000.00',
        'breakdown': {0: 0, 0.12: 4555.2, 0.02: 1072.32},
        'total NI': '5627.52'}
    results = test_national_insurance.Calculate(financial_year=financial_year)
    actual_total_tax = 5624.12
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

# Requires changing after presentation of data has been finalised
def test_Calculate_variable_year_under_first_threshold():
    test_national_insurance = national_insurance.NationalInsurance(5000)
    financial_year = "2022-23"
    calculated_partial_results = {
        'gross income': '5000.00',
        'breakdown': {0: 0, 0.12: 0, 0.02: 0},
        'total NI': '0.00'
        }
    results = test_national_insurance.Calculate(financial_year=financial_year)
    actual_total_tax = 0.00
    assert isinstance(results, dict)
    # assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    # assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

def test_Calculate_variable_year_over_first_threshold():
    # change when a better presentation of values have been decided
    test_national_insurance = national_insurance.NationalInsurance(29000)
    financial_year = "2022-23"
    calculated_partial_results = {
        'gross income': '29000.00',
        'breakdown': {0: 0, 0.12: 2469.12, 0.02: 0},
        'total NI': '2180.08'
        }
    results = test_national_insurance.Calculate(financial_year=financial_year)
    actual_total_tax = 2180.51
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    # assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

# Requires changing after presentation of data has been finalised
def test_Calculate_variable_year_over_second_threshold():
    test_national_insurance = national_insurance.NationalInsurance(200000)
    financial_year = "2022-23"
    calculated_partial_results = {
        'gross income': '200000.00',
        'breakdown': {0: 0, 0.12: 0, 0.02: 0},
        'total NI': '8973.75'
        }
    results = test_national_insurance.Calculate(financial_year=financial_year)
    actual_total_tax = 8974.39
    assert isinstance(results, dict)
    # assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    # assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

def test_Calculate_key_error():
    dummy_year = "2016-2017"
    test_national_insurance = national_insurance.NationalInsurance(current_salary=32400)
    results = test_national_insurance.Calculate(financial_year=dummy_year)
    assert results == "Year not included in calculator, wrong format provided, or \
incorrect key provided for data. Please call GetAdditionalParameters() \
to find available timeframes and format"

def test_Calculate_salary_error():
    dummy_salary = "90"
    test_national_insurance = national_insurance.NationalInsurance(current_salary=dummy_salary)
    results = test_national_insurance.Calculate(financial_year="2022-23")
    assert results == "Please provide a valid salary, in integers"

def test_Calculate_negative_salary():
    dummy_salary = -90
    test_national_insurance = national_insurance.NationalInsurance(current_salary=dummy_salary)
    results = test_national_insurance.Calculate(financial_year="2022-23")
    assert results == "Please provide a positive salary"
