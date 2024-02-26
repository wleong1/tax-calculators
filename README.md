# **tax-calculators**

Tax-calculators is a all-in-one calculator where users can calculate the total tax paid per year.

## Table of Contents

- [Project Description](#project-description)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Tests](#tests)
- [Contributing](#contributing)
- [License](#license)

## Project Description

The tax-calculators is a comprehensive collection of income tax calculators designed to simplify financial planning and budgeting. 
This suite offers a range of calculators tailored to different tax systems, providing users with accurate estimates of their tax liabilities based on various income sources and financial scenarios.

## Technologies

- Python 3.10
- Numpy
- Pandas
- Pytest
- Click
- Textual
- Rich
- PrettyTable

## **Installation**

1. Clone the project repository using Git.
2. cd into the cloned repository.
```cd tax-calculators/```.
3. Ensure that docker is installed.
```docker --version```
If docker is not installed, head [here](https://docs.docker.com/get-docker/) to install. 
4. Build the docker image.
```docker build -t calc_ui .```

## **Usage**

1. Run the docker image.
```docker run -it calc_ui```
2. To run the user interfaces:
```python3 cli/calculators_cli.py``` for Command-Line Interface (CLI)
*or*
```python3 tui/calculators_tui.py``` for Text User Interface (TUI)
    
Note: 
- This project is still ongoing and more calculators will be added in the future.

## **Screenshots**

The image showcases the Command-Line Interface.
![image](https://github.com/wleong1/tax-calculators/blob/main/images/Command-Line%20Interface.png)

The image showcases the Command-Line Interface.
![image](https://github.com/wleong1/tax-calculators/blob/main/images/Text%20User%20Interface.png)


## **Tests**

Tax-calculators incorporates various tests to ensure its stability and reliability. To execute these tests, follow these steps:

1. To run the tests within the **tests** folder:
```pytest tests/```
2. To check the code coverage of the tests:
```pytest --cov=src```

## **Contributing**

Contributions to StockTracker are welcome! If you'd like to contribute, please follow these guidelines:

1. Fork the project.
2. Create your feature branch (git checkout -b feature/your-feature-name).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/your-feature-name).
5. Open a pull request.

# **License**

This project is licensed under the MIT License.
