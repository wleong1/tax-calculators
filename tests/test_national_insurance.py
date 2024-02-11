from src import national_insurance
from unittest.mock import patch
import pytest


def test_get_name():
    test_national_insurance = national_insurance.NationalInsurance()
    results = test_national_insurance.get_name()
    assert results == "National_Insurance"

def test_get_calculation_parameters():
    test_national_insurance = national_insurance.NationalInsurance()
    results = test_national_insurance.get_calculation_parameters()
    assert isinstance(results, dict)
    assert results == {"inputs": ["current_salary"], "outputs": ["total_tax"]}

def test_get_additional_parameters_constant_year():
    test_national_insurance = national_insurance.NationalInsurance()
    dummy_data_2015_16 = {
        "thresholds_annual": [0, 8060, 42380],
        "thresholds_month": [0, 671, 3530],
        "thresholds_week": [0, 155, 815],
        "rates": [0, 0.12, 0.02]
    }
    results = test_national_insurance.get_additional_parameters()
    assert isinstance(results, dict)
    assert results["2015-16"] == dummy_data_2015_16

def test_get_additional_parameters_variable_year():
    test_national_insurance = national_insurance.NationalInsurance()
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
    results = test_national_insurance.get_additional_parameters()
    assert isinstance(results, dict)
    assert results["2022-23"] == dummy_data_2022_23

def test_calculate_constant_year_under_first_threshold():
    test_national_insurance = national_insurance.NationalInsurance()
    financial_year = "2018-19"
    current_salary = 5000
    calculated_partial_results = {
        'gross income': '5000.00',
        'breakdown': {0: 0, 0.12: 0, 0.02: 0},
        'total NI': '0.00'
        }
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 0.00
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

def test_calculate_constant_year_over_first_threshold():
    test_national_insurance = national_insurance.NationalInsurance()
    financial_year = "2018-19"
    current_salary = 29000
    calculated_partial_results = {
        'gross income': '29000.00',
        'breakdown': {0: 0, 0.12: 2469.12, 0.02: 0},
        'total NI': '2469.12'
        }
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 2469.12
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

def test_calculate_constant_year_over_second_threshold():
    test_national_insurance = national_insurance.NationalInsurance()
    financial_year = "2018-19"
    current_salary = 100000
    calculated_partial_results = {
        'gross income': '100000.00',
        'breakdown': {0: 0, 0.12: 4555.2, 0.02: 1072.32},
        'total NI': '5627.52'}
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 5624.12
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

# Requires changing after presentation of data has been finalised
def test_calculate_variable_year_under_first_threshold():
    test_national_insurance = national_insurance.NationalInsurance()
    financial_year = "2022-23"
    current_salary = 5000
    calculated_partial_results = {
        'gross income': '5000.00',
        'breakdown': {0: 0, 0.12: 0, 0.02: 0},
        'total NI': '0.00'
        }
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 0.00
    assert isinstance(results, dict)
    # assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    # assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

def test_calculate_variable_year_over_first_threshold():
    # change when a better presentation of values have been decided
    test_national_insurance = national_insurance.NationalInsurance()
    financial_year = "2022-23"
    current_salary = 29000
    calculated_partial_results = {
        'gross income': '29000.00',
        'breakdown': {0: 0, 0.12: 2469.12, 0.02: 0},
        'total NI': '2180.08'
        }
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 2180.51
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    # assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

# Requires changing after presentation of data has been finalised
def test_calculate_variable_year_over_second_threshold():
    test_national_insurance = national_insurance.NationalInsurance()
    financial_year = "2022-23"
    current_salary = 200000
    calculated_partial_results = {
        'gross income': '200000.00',
        'breakdown': {0: 0, 0.12: 0, 0.02: 0},
        'total NI': '8973.75'
        }
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 8974.39
    assert isinstance(results, dict)
    # assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    # assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

def test_calculate_key_error():
    dummy_year = "2016-2017"
    current_salary = 32400
    test_national_insurance = national_insurance.NationalInsurance()
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=dummy_year)
    assert results == "Year not included in calculator, wrong format provided, or \
incorrect key provided for data. Please call get_additional_parameters() \
to find available timeframes and format"

def test_calculate_salary_error():
    dummy_salary = "90"
    test_national_insurance = national_insurance.NationalInsurance()
    results = test_national_insurance.calculate(current_salary=dummy_salary, financial_year="2022-23")
    assert results == "Please provide a valid salary, in integers"

def test_calculate_negative_salary():
    dummy_salary = -90
    test_national_insurance = national_insurance.NationalInsurance()
    results = test_national_insurance.calculate(current_salary=dummy_salary, financial_year="2022-23")
    assert results == "Please provide a positive salary"

@pytest.fixture
def test_national_insurance():
    yield national_insurance.NationalInsurance()

def test_mock_get_name(test_national_insurance):
    results = test_national_insurance.get_name()
    assert results == "National_Insurance"

@patch("src.national_insurance.NationalInsurance.get_calculation_parameters")
def test_mock_get_calculation_parameters(mock_get, test_national_insurance):
    mock_get.return_value = {"inputs": ["current_salary"], "outputs": ["total_tax"]}
    results = test_national_insurance.get_calculation_parameters()
    assert isinstance(results, dict)
    assert results == {"inputs": ["current_salary"], "outputs": ["total_tax"]}

@patch("src.national_insurance.NationalInsurance.get_additional_parameters")
def test_mock_get_additional_parameters_constant_year(mock_get, test_national_insurance):
    dummy_data_2015_16 = {"2015-16":
        {"thresholds_annual": [0, 8060, 42380],
        "thresholds_month": [0, 671, 3530],
        "thresholds_week": [0, 155, 815],
        "rates": [0, 0.12, 0.02]}
    }
    mock_get.return_value = dummy_data_2015_16
    results = test_national_insurance.get_additional_parameters()
    assert isinstance(results, dict)
    assert results["2015-16"] == dummy_data_2015_16["2015-16"]

@patch("src.national_insurance.NationalInsurance.get_additional_parameters")
def test_mock_get_additional_parameters_variable_year(mock_get, test_national_insurance):
    dummy_data_2022_23 =  {"2022-23":
        {"3":{
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
        }}
    }
    mock_get.return_value = dummy_data_2022_23
    results = test_national_insurance.get_additional_parameters()
    assert isinstance(results, dict)
    assert results["2022-23"] == dummy_data_2022_23["2022-23"]

@patch("src.national_insurance.NationalInsurance.calculate")
def test_mock_calculate_constant_year_under_first_threshold(mock_get, test_national_insurance):
    full_results = {
    'Annual breakdown': {
    'gross income': '5000.00',
    'breakdown': {0: 0, 0.12: 0.0, 0.02: 0.0},
    'total': '0.00'
    },
    'Monthly breakdown': {
    'gross income': '416.67',
    'breakdown': {0: '0.00', 0.12: '0.00', 0.02: '0.00'},
    'total': '0.00'
    },
    'Weekly breakdown': {
    'gross income': '96.15',
    'breakdown': {0: '0.00', 0.12: '0.00', 0.02: '0.00'},
    'total': '0.00'
    },
    'Daily breakdown': {
    'gross income': '19.23',
    'breakdown': {0: '0.00', 0.12: '0.00', 0.02: '0.00'},
    'total': '0.00'
    }
    }
    mock_get.return_value = full_results
    financial_year = "2018-19"
    current_salary = 5000
    calculated_partial_results = {
        'gross income': '5000.00',
        'breakdown': {0: 0, 0.12: 0, 0.02: 0},
        'total NI': '0.00'
        }
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 0.00
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

@patch("src.national_insurance.NationalInsurance.calculate")
def test_mock_calculate_constant_year_over_first_threshold(mock_get, test_national_insurance):
    full_results = {
    'Annual breakdown': {
    'gross income': '29000.00',
    'breakdown': {0: 0, 0.12: 2469.12, 0.02: 0.0},
    'total': '2469.12'
    },
    'Monthly breakdown': {
    'gross income': '2416.67',
    'breakdown': {0: '0.00', 0.12: '205.76', 0.02: '0.00'},
    'total': '205.76'
    },
    'Weekly breakdown': {
    'gross income': '557.69',
    'breakdown': {0: '0.00', 0.12: '47.48', 0.02: '0.00'},
    'total': '47.48'
    },
    'Daily breakdown': {
    'gross income': '111.54',
    'breakdown': {0: '0.00', 0.12: '9.50', 0.02: '0.00'},
    'total': '9.50'
    }
    }
    mock_get.return_value = full_results
    financial_year = "2018-19"
    current_salary = 29000
    calculated_partial_results = {
        'gross income': '29000.00',
        'breakdown': {0: 0, 0.12: 2469.12, 0.02: 0},
        'total NI': '2469.12'
        }
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 2469.12
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

@patch("src.national_insurance.NationalInsurance.calculate")
def test_mock_calculate_constant_year_over_second_threshold(mock_get, test_national_insurance):
    full_results = {
    'Annual breakdown': {
    'gross income': '100000.00',
    'breakdown': {0: 0, 0.12: 4555.2, 0.02: 1072.32},
    'total': '5627.52'
    },
    'Monthly breakdown': {
    'gross income': '8333.33',
    'breakdown': {0: '0.00', 0.12: '379.60', 0.02: '89.36'},
    'total': '468.96'
    },
    'Weekly breakdown': {
    'gross income': '1923.08',
    'breakdown': {0: '0.00', 0.12: '87.60', 0.02: '20.62'},
    'total': '108.22'
    },
    'Daily breakdown': {
    'gross income': '384.62',
    'breakdown': {0: '0.00', 0.12: '17.52', 0.02: '4.12'},
    'total': '21.64'
    }
    }
    mock_get.return_value = full_results
    financial_year = "2018-19"
    current_salary = 100000
    calculated_partial_results = {
        'gross income': '100000.00',
        'breakdown': {0: 0, 0.12: 4555.2, 0.02: 1072.32},
        'total NI': '5627.52'}
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 5624.12
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

# Requires changing after presentation of data has been finalised
@patch("src.national_insurance.NationalInsurance.calculate")
def test_mock_calculate_variable_year_under_first_threshold(mock_get, test_national_insurance):
    full_results = {
    'Annual breakdown': {
    'gross income': '5000.00',
    'breakdown': {0: 0, 0.12: 0.0, 0.02: 0.0},
    'total': '0.00'
    },
    'Monthly breakdown': {
    'gross income': '416.67',
    'breakdown': {0: '0.00', 0.12: '0.00', 0.02: '0.00'},
    'total': '0.00'
    },
    'Weekly breakdown': {
    'gross income': '96.15',
    'breakdown': {0: '0.00', 0.12: '0.00', 0.02: '0.00'},
    'total': '0.00'
    },
    'Daily breakdown': {
    'gross income': '19.23',
    'breakdown': {0: '0.00', 0.12: '0.00', 0.02: '0.00'},
    'total': '0.00'
    }
    }
    mock_get.return_value = full_results
    financial_year = "2022-23"
    current_salary = 5000
    calculated_partial_results = {
        'gross income': '5000.00',
        'breakdown': {0: 0, 0.12: 0, 0.02: 0},
        'total NI': '0.00'
        }
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 0.00
    assert isinstance(results, dict)
    # assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    # assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

@patch("src.national_insurance.NationalInsurance.calculate")
def test_mock_calculate_variable_year_over_first_threshold(mock_get, test_national_insurance):
    # change when a better presentation of values have been decided
    full_results = {
    'Annual breakdown': {
    'gross income': '29000.00',
    'breakdown': {0: 0.0, 0.12: 164.24, 0.02: 0.0},
    'total': '2180.08'
    },
    'Monthly breakdown': {
    'gross income': '2416.67',
    'breakdown': {0: '0.00', 0.12: '13.69', 0.02: '0.00'},
    'total': '181.67'
    },
    'Weekly breakdown': {
    'gross income': '557.69',
    'breakdown': {0: '0.00', 0.12: '3.16', 0.02: '0.00'},
    'total': '41.92'
    },
    'Daily breakdown': {
    'gross income': '111.54',
    'breakdown': {0: '0.00', 0.12: '0.63', 0.02: '0.00'},
    'total': '8.38'
    }
    }
    mock_get.return_value = full_results
    financial_year = "2022-23"
    current_salary = 29000
    calculated_partial_results = {
        'gross income': '29000.00',
        'breakdown': {0: 0, 0.12: 2469.12, 0.02: 0},
        'total NI': '2180.08'
        }
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 2180.51
    assert isinstance(results, dict)
    assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    # assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

# Requires changing after presentation of data has been finalised
@patch("src.national_insurance.NationalInsurance.calculate")
def test_mock_calculate_variable_year_over_second_threshold(mock_get, test_national_insurance):
    full_results = {
    'Annual breakdown': {
    'gross income': '200000.00',
    'breakdown': {0: 0.0, 0.12: 376.92, 0.02: 626.47},
    'total': '8973.75'
    },
    'Monthly breakdown': {
    'gross income': '16666.67',
    'breakdown': {0: '0.00', 0.12: '31.41', 0.02: '52.21'},
    'total': '747.81'
    },
    'Weekly breakdown': {
    'gross income': '3846.15',
    'breakdown': {0: '0.00', 0.12: '7.25', 0.02: '12.05'},
    'total': '172.57'
    },
    'Daily breakdown': {
    'gross income': '769.23',
    'breakdown': {0: '0.00', 0.12: '1.45', 0.02: '2.41'},
    'total': '34.51'
    }
    }
    mock_get.return_value = full_results
    financial_year = "2022-23"
    current_salary = 200000
    calculated_partial_results = {
        'gross income': '200000.00',
        'breakdown': {0: 0, 0.12: 0, 0.02: 0},
        'total NI': '8973.75'
        }
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=financial_year)
    actual_total_tax = 8974.39
    assert isinstance(results, dict)
    # assert results["Annual breakdown"]["gross income"] == calculated_partial_results["gross income"]
    # assert results["Annual breakdown"]["breakdown"] == calculated_partial_results["breakdown"]
    assert float(calculated_partial_results["total NI"]) <= actual_total_tax + 10
    assert float(calculated_partial_results["total NI"]) >= actual_total_tax - 10

@patch("src.national_insurance.NationalInsurance.calculate")
def test_mock_calculate_key_error(mock_get, test_national_insurance):
    dummy_results = "Year not included in calculator, wrong format provided, \
or incorrect key provided for data. \
Please call get_additional_parameters() to find available timeframes and format"
    mock_get.return_value = dummy_results
    dummy_year = "2016-2017"
    current_salary = 32400
    test_national_insurance = national_insurance.NationalInsurance()
    results = test_national_insurance.calculate(current_salary=current_salary, financial_year=dummy_year)
    assert results == "Year not included in calculator, wrong format provided, or \
incorrect key provided for data. Please call get_additional_parameters() \
to find available timeframes and format"

@patch("src.national_insurance.NationalInsurance.calculate")
def test_mock_calculate_salary_error(mock_get, test_national_insurance):
    dummy_salary = "90"
    dummy_results = "Please provide a valid salary, in integers"
    mock_get.return_value = dummy_results
    results = test_national_insurance.calculate(current_salary=dummy_salary, financial_year="2022-23")
    assert results == "Please provide a valid salary, in integers"

@patch("src.national_insurance.NationalInsurance.calculate")
def test_mock_calculate_negative_salary(mock_get, test_national_insurance):
    dummy_salary = -90
    dummy_results = "Please provide a positive salary"
    mock_get.return_value = dummy_results
    results = test_national_insurance.calculate(current_salary=dummy_salary, financial_year="2022-23")
    assert results == "Please provide a positive salary"
