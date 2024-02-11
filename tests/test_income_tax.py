from src import income_tax
from unittest.mock import patch
import pytest

def test_get_name():
    test_income_tax = income_tax.IncomeTax()
    results = test_income_tax.get_name()
    assert results == "Income_Tax"

def test_get_calculation_parameters():
    test_income_tax = income_tax.IncomeTax()
    results = test_income_tax.get_calculation_parameters()
    assert isinstance(results, dict)
    assert results == {"inputs": ["current_salary"], "outputs": ["total_tax"]}

def test_get_additional_parameters():
    test_income_tax = income_tax.IncomeTax()
    dummy_data = {
        "personal_allowance": 11000,
        "personal_allowance threshold": 100000,
        "thresholds": [0, 11000, 43000, 150000],
        "rates": [0, 0.2, 0.4, 0.45]
    }
    results = test_income_tax.get_additional_parameters()
    assert isinstance(results, dict)
    assert results["2016-17"] == dummy_data

def test_calculate_under_first_threshold():
    test_income_tax = income_tax.IncomeTax()
    financial_year = "2022-23"
    current_salary = 12570
    calculated_partial_results = {
        'gross income': '12570.00',
        'breakdown': {0: '0.00', 0.2: '0.00', 0.4: '0.00', 0.45: '0.00'},
        'total income tax': '0.00'
        }
    results = test_income_tax.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 0.00
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_calculate_over_first_threshold():
    test_income_tax = income_tax.IncomeTax()
    financial_year = "2022-23"
    current_salary = 29000
    calculated_partial_results = {
        'gross income': '29000.00',
        'breakdown': {0: "0.00", 0.2: "3286.00", 0.4: "0.00", 0.45: "0.00"},
        'total income tax': '3286.00'
        }
    results = test_income_tax.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 3286
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_calculate_over_second_threshold():
    test_income_tax = income_tax.IncomeTax()
    financial_year = "2022-23"
    current_salary = 60000
    calculated_partial_results = {
        'gross income': '60000.00',
        'breakdown': {0: "0.00", 0.2: "7540.00", 0.4: "3892.00", 0.45: "0.00"},
        'total income tax': '11432.00'
        }
    results = test_income_tax.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 11432
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_calculate_over_third_threshold():
    test_income_tax = income_tax.IncomeTax()
    financial_year = "2022-23"
    current_salary = 102000
    calculated_partial_results = {
        'gross income': '102000.00',
        'breakdown': {0: "0.00", 0.2: "7540.00", 0.4: "21092.00", 0.45: "0.00"},
        'total income tax': '28632.00'
        }
    results = test_income_tax.calculate(current_salary = current_salary, financial_year=financial_year)
    actual_total_tax = 28632
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_calculate_zero_personal_allowance():
    test_income_tax = income_tax.IncomeTax()
    financial_year = "2021-22"
    current_salary = 200000
    calculated_partial_results = {
        'gross income': '200000.00',
        'breakdown': {0.2: "7540.00", 0.4: "44920.00", 0.45: "22500.00"},
        'total income tax': '74960.00'
        }
    results = test_income_tax.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 74960
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

def test_calculate_wrong_argument_format():
    test_income_tax = income_tax.IncomeTax()
    dummy_financial_year = "2022/23"
    current_salary = 29000
    results = test_income_tax.calculate(current_salary=current_salary, financial_year=dummy_financial_year)
    assert results == "Year not included in calculator, wrong format provided, \
or incorrect key provided for data. \
Please call get_additional_parameters() to find available timeframes and format"

def test_calculate_salary_error():
    dummy_salary = "90"
    test_income_tax = income_tax.IncomeTax()
    results = test_income_tax.calculate(current_salary=dummy_salary, financial_year="2022-23")
    assert results == "Please provide a valid salary, in integers"

def test_calculate_negative_salary():
    dummy_salary = -90
    test_income_tax = income_tax.IncomeTax()
    results = test_income_tax.calculate(current_salary = dummy_salary, financial_year="2022-23")
    assert results == "Please provide a positive salary"

@pytest.fixture
def test_income_tax():
    yield income_tax.IncomeTax()

def test_mock_get_name(test_income_tax):
    results = test_income_tax.get_name()
    assert results == "Income_Tax"

@patch("src.income_tax.IncomeTax.get_calculation_parameters")
def test_mock_get_calculation_parameters(mock_get, test_income_tax):
    mock_get.return_value = {"inputs": ["current_salary"], "outputs": ["total_tax"]}
    results = test_income_tax.get_calculation_parameters()
    assert isinstance(results, dict)
    assert results == {"inputs": ["current_salary"], "outputs": ["total_tax"]}

@patch("src.income_tax.IncomeTax.get_additional_parameters")
def test_mock_get_additional_parameters(mock_get, test_income_tax):
    dummy_data = {"2016-17":
        {"personal_allowance": 11000,
        "personal_allowance threshold": 100000,
        "thresholds": [0, 11000, 43000, 150000],
        "rates": [0, 0.2, 0.4, 0.45]}
    }
    mock_get.return_value = dummy_data
    results = test_income_tax.get_additional_parameters()
    assert isinstance(results, dict)
    assert results["2016-17"] == dummy_data["2016-17"]

@patch("src.income_tax.IncomeTax.calculate")
def test_mock_calculate_under_first_threshold(mock_get, test_income_tax):
    full_results = {
    'Annual breakdown': {
    'gross income': '12570.00',
    'breakdown': {0: '0.00', 0.2: '0.00', 0.4: '0.00', 0.45: '0.00'},
    'total': '0.00'
    },
    'Monthly breakdown': {
    'gross income': '1047.50',
    'breakdown': {0: '0.00', 0.2: '0.00', 0.4: '0.00', 0.45: '0.00'},
    'total': '0.00'
    },
    'Weekly breakdown': {
    'gross income': '241.73',
    'breakdown': {0: '0.00', 0.2: '0.00', 0.4: '0.00', 0.45: '0.00'},
    'total': '0.00'
    },
    'Daily breakdown': {
    'gross income': '48.35',
    'breakdown': {0: '0.00', 0.2: '0.00', 0.4: '0.00', 0.45: '0.00'},
    'total': '0.00'
    }
    }
    mock_get.return_value = full_results
    financial_year = "2022-23"
    current_salary = 12570
    calculated_partial_results = {
        'gross income': '12570.00',
        'breakdown': {0: '0.00', 0.2: '0.00', 0.4: '0.00', 0.45: '0.00'},
        'total income tax': '0.00'
        }
    results = test_income_tax.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 0.00
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

@patch("src.income_tax.IncomeTax.calculate")
def test_mock_calculate_over_first_threshold(mock_get, test_income_tax):
    full_results = {
    'Annual breakdown': {
    'gross income': '29000.00',
    'breakdown': {0: '0.00', 0.2: '3286.00', 0.4: '0.00', 0.45: '0.00'},
    'total': '0.00'
    },
    'Monthly breakdown': {
    'gross income': '2416.67',
    'breakdown': {0: '0.00', 0.2: '273.83', 0.4: '0.00', 0.45: '0.00'},
    'total': '273.83'
    },
    'Weekly breakdown': {
    'gross income': '557.69',
    'breakdown': {0: '0.00', 0.2: '63.19', 0.4: '0.00',0.45: '0.00'},
    'total': '63.19'
    },
    'Daily breakdown': {
    'gross income': '111.54',
    'breakdown': {0: '0.00', 0.2: '12.64', 0.4: '0.00', 0.45: '0.00'},
    'total': '12.64'
    }
    }
    mock_get.return_value = full_results
    financial_year = "2022-23"
    current_salary = 29000
    calculated_partial_results = {
        'gross income': '29000.00',
        'breakdown': {0: "0.00", 0.2: "3286.00", 0.4: "0.00", 0.45: "0.00"},
        'total income tax': '3286.00'
        }
    results = test_income_tax.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 3286
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

@patch("src.income_tax.IncomeTax.calculate")
def test_mock_calculate_over_second_threshold(mock_get, test_income_tax):
    full_results = {
    'Annual breakdown': {
    'gross income': '60000.00',
    'breakdown': {0: '0.00', 0.2: '7540.00', 0.4: '3892.00', 0.45: '0.00'},
    'total': '11432.00'
    },
    'Monthly breakdown': {
    'gross income': '5000.00',
    'breakdown': {0: '0.00', 0.2: '628.33', 0.4: '324.33', 0.45: '0.00'},
    'total': '952.67'
    },
    'Weekly breakdown': {
    'gross income': '1153.85',
    'breakdown': {0: '0.00', 0.2: '145.00', 0.4: '74.85', 0.45: '0.00'},
    'total': '219.85'
    },
    'Daily breakdown': {
    'gross income': '230.77',
    'breakdown': {0: '0.00', 0.2: '29.00', 0.4: '14.97', 0.45: '0.00'},
    'total': '43.97'
    }
    }
    mock_get.return_value = full_results
    financial_year = "2022-23"
    current_salary = 60000
    calculated_partial_results = {
        'gross income': '60000.00',
        'breakdown': {0: "0.00", 0.2: "7540.00", 0.4: "3892.00", 0.45: "0.00"},
        'total income tax': '11432.00'
        }
    results = test_income_tax.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 11432
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

@patch("src.income_tax.IncomeTax.calculate")
def test_mock_calculate_over_third_threshold(mock_get, test_income_tax):
    full_results = {
    'Annual breakdown': {
    'gross income': '102000.00',
    'breakdown': {0: '0.00', 0.2: '7540.00', 0.4: '21092.00', 0.45: '0.00'},
    'total': '28632.00'
    },
    'Monthly breakdown': {
    'gross income': '8500.00', 
    'breakdown': {0: '0.00', 0.2: '628.33', 0.4: '1757.67', 0.45: '0.00'},
    'total': '2386.00'
    },
    'Weekly breakdown': {
    'gross income': '1961.54',
    'breakdown': {0: '0.00', 0.2: '145.00', 0.4: '405.62', 0.45: '0.00'},
    'total': '550.62'
    },
    'Daily breakdown': {
    'gross income': '392.31',
    'breakdown': {0: '0.00', 0.2: '29.00', 0.4: '81.12', 0.45: '0.00'},
    'total': '110.12'
    }
    }
    mock_get.return_value = full_results
    financial_year = "2022-23"
    current_salary = 102000
    calculated_partial_results = {
        'gross income': '102000.00',
        'breakdown': {0: "0.00", 0.2: "7540.00", 0.4: "21092.00", 0.45: "0.00"},
        'total income tax': '28632.00'
        }
    results = test_income_tax.calculate(current_salary = current_salary, financial_year=financial_year)
    actual_total_tax = 28632
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

@patch("src.income_tax.IncomeTax.calculate")
def test_mock_calculate_zero_personal_allowance(mock_get, test_income_tax):
    full_results = {
    'Annual breakdown': {
    'gross income': '200000.00',
    'breakdown': {0.2: '7540.00', 0.4: '44920.00', 0.45: '22500.00'},
    'total': '74960.00'
    },
    'Monthly breakdown': {
    'gross income': '16666.67',
    'breakdown': {0.2: '628.33', 0.4: '3743.33', 0.45: '1875.00'},
    'total': '6246.67'
    },
    'Weekly breakdown': {
    'gross income': '3846.15',
    'breakdown': {0.2: '145.00', 0.4: '863.85', 0.45: '432.69'},
    'total': '1441.54'
    },
    'Daily breakdown': {
    'gross income': '769.23',
    'breakdown': {0.2: '29.00', 0.4: '172.77', 0.45: '86.54'},
    'total': '288.31'
    }
    }
    mock_get.return_value = full_results
    financial_year = "2022-23"
    current_salary = 200000
    calculated_partial_results = {
        'gross income': '200000.00',
        'breakdown': {0.2: "7540.00", 0.4: "44920.00", 0.45: "22500.00"},
        'total income tax': '74960.00'
        }
    results = test_income_tax.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 74960
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total income tax"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total income tax"]) >= actual_total_tax - 10

@patch("src.income_tax.IncomeTax.calculate")
def test_mock_calculate_wrong_argument_format(mock_get, test_income_tax):
    dummy_results = "Year not included in calculator, wrong format provided, \
or incorrect key provided for data. \
Please call get_additional_parameters() to find available timeframes and format"
    mock_get.return_value = dummy_results
    dummy_financial_year = "2022/23"
    current_salary = 29000
    results = test_income_tax.calculate(current_salary=current_salary, financial_year=dummy_financial_year)
    assert results == "Year not included in calculator, wrong format provided, \
or incorrect key provided for data. \
Please call get_additional_parameters() to find available timeframes and format"

@patch("src.income_tax.IncomeTax.calculate")
def test_mock_calculate_salary_error(mock_get, test_income_tax):
    dummy_salary = "90"
    dummy_results = "Please provide a valid salary, in integers"
    mock_get.return_value = dummy_results
    results = test_income_tax.calculate(current_salary=dummy_salary, financial_year="2022-23")
    assert results == "Please provide a valid salary, in integers"

@patch("src.income_tax.IncomeTax.calculate")
def test_mock_calculate_negative_salary(mock_get, test_income_tax):
    dummy_salary = -90
    dummy_results = "Please provide a positive salary"
    mock_get.return_value = dummy_results
    results = test_income_tax.calculate(current_salary = dummy_salary, financial_year="2022-23")
    assert results == "Please provide a positive salary"
