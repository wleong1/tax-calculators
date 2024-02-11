"""This module provides the necessary information for national insurance calculations."""
information: dict = {
    "2015-16": {
        "thresholds_annual": [0, 8060, 42380],
        "thresholds_month": [0, 671, 3530],
        "thresholds_week": [0, 155, 815],
        "rates": [0, 0.12, 0.02]
    },
    "2016-17": {
        "thresholds_annual": [0, 8060, 43004],
        "thresholds_month": [0, 671, 3582],
        "thresholds_week": [0, 155, 827],
        "rates": [0, 0.12, 0.02]
    },
    "2017-18": {
        "thresholds_annual": [0, 8164, 45032],
        "thresholds_month": [0, 680, 3751],
        "thresholds_week": [0, 157, 866],
        "rates": [0, 0.12, 0.02]
    },
    "2018-19": {
        "thresholds_annual": [0, 8424, 46384],
        "thresholds_month": [0, 701, 3864],
        "thresholds_week": [0, 162, 892],
        "rates": [0, 0.12, 0.02]
    },
    "2019-20": {
        "thresholds_annual": [0, 8632, 50024],
        "thresholds_month": [0, 719, 4167],
        "thresholds_week": [0, 166, 962],
        "rates": [0, 0.12, 0.02]
    },
    "2020-21": {
        "thresholds_annual": [0, 9516, 50024],
        "thresholds_month": [0, 792, 4167],
        "thresholds_week": [0, 183, 962],
        "rates": [0, 0.12, 0.02]
    },
    "2021-22": {
        "thresholds_annual": [0, 9568, 50284],
        "thresholds_month": [0, 797, 4189],
        "thresholds_week": [0, 184, 967],
        "rates": [0, 0.12, 0.02]
    },
    # Maybe combine all of below and show how much it is per period in breakdown
    # What logic should I implement to detect multiple rates in a year?
    # List of lists? another keyword for time period?
    # How to calculate and combine?
    "2022-23": {
        # "6th April to 5th July":{
        "3":{
        # "thresholds_annual": [0, 9880, 50284],
        "thresholds_month": [0, 823, 4189],
        "thresholds_week": [0, 190, 967],
        "rates": [0, 0.1325, 0.0325]
        },
    # Below might need changing, work out how much the thresholds and rates are from the website
        # "6th July to 5th November":{
        "4":{
        # "thresholds_annual": [0, 12584, 50284],
        "thresholds_month": [0, 1048, 4189],
        "thresholds_week": [0, 242, 967],
        "rates": [0, 0.1325, 0.0325]
        },
        # "6th November to 5th April":{
        "5":{
        # "thresholds_annual": [0, 12584, 50284],
        "thresholds_month": [0, 1048, 4189],
        "thresholds_week": [0, 242, 967],
        "rates": [0, 0.12, 0.02]
        }
    },
    "2023-24": {
        # "6th April to 5th January":{
        # "thresholds_annual": [0, 12570, 50270],
        "9":{
        "thresholds_month": [0, 1049, 4189],
        "thresholds_week": [0, 242, 967],
        "rates": [0, 0.12, 0.02]
        },
        # "6th January to 5th April":{
        # "thresholds_annual": [0, 12570, 50270],
        "3":{
        "thresholds_month": [0, 1049, 4189],
        "thresholds_week": [0, 242, 967],
        "rates": [0, 0.10, 0.02]
        }
    }
}
