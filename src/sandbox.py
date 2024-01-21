# a = 242
# print(a, a*52/12, a*52)
# print(12570/12, 12570/52)
import income_tax_info
data = income_tax_info.information
financial_year_data = data["2022-23"]
thresholds, rates = financial_year_data["thresholds"], financial_year_data["rates"]
thresholds[1] -= 1000
print(thresholds, financial_year_data, data["2022-23"])

data_two = {'personal_allowance': 12570, 'personal_allowance threshold': 100000, 'thresholds': [0, 12570, 50270, 150000], 'rates': [0, 0.2, 0.4, 0.45]}
thresholds_two, rates_two = data_two["thresholds"], data_two["rates"]
thresholds_two[1] -= 1000
print(thresholds_two, data_two)