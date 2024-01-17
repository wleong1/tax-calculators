class TaxCode:
    def __init__(self) -> None:
        self.tax_codes = {"L", "0T", "M", "N", "T", "BR"}

    def provide_params(self, suffix, prefix):
        if suffix == "L":
            amount = int(prefix + "0")
            thresholds = [0, amount, amount + 37700, 125140]
            rates = [0, 0.2, 0.4, 0.45]
            return thresholds, rates
        

information = {
    "2015-16": {
        "personal allowance": 10600,
        "personal allowance threshold": 100000,
        "thresholds": [0, 10600, 31785, 150000],
        "rates": [0, 0.2, 0.4, 0.45]        
    },
    "2016-17": {
        "personal allowance": 11000,
        "personal allowance threshold": 100000,
        "thresholds": [0, 11000, 32000, 150000],
        "rates": [0, 0.2, 0.4, 0.45]        
    },
    "2017-18": {
        "personal allowance": 11500,
        "personal allowance threshold": 100000,
        "thresholds": [0, 11500, 33500, 150000],
        "rates": [0, 0.2, 0.4, 0.45]        
    },
    "2018-19": {
        "personal allowance": 11850,
        "personal allowance threshold": 100000,
        "thresholds": [0, 11850, 34500, 150000],
        "rates": [0, 0.2, 0.4, 0.45]        
    },
    "2019-20": {
        "personal allowance": 12500,
        "personal allowance threshold": 100000,
        "thresholds": [0, 12500, 37500, 150000],
        "rates": [0, 0.2, 0.4, 0.45]        
    },
    "2020-21": {
        "personal allowance": 12500,
        "personal allowance threshold": 100000,
        "thresholds": [0, 12500, 37500, 150000],
        "rates": [0, 0.2, 0.4, 0.45]        
    },
    "2021-22": {
        "personal allowance": 12570,
        "personal allowance threshold": 100000,
        "thresholds": [0, 12570, 37700, 150000],
        "rates": [0, 0.2, 0.4, 0.45]        
    },
    "2022-23": {
        "personal allowance": 12570,
        "personal allowance threshold": 100000,
        "thresholds": [0, 12570, 37700, 150000],
        "rates": [0, 0.2, 0.4, 0.45]        
    },
    "2023-24": {
        "personal allowance": 12570,
        "personal allowance threshold": 100000,
        "thresholds": [0, 12570, 37700, 150000],
        "rates": [0, 0.2, 0.4, 0.45]        
    }    
}