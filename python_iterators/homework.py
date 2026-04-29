"""
1. You're going to write an interactive calculator! User input is assumed to be a formula that consist of a number,
an operator (at least + and -), and another number, separated by white space (e.g. 1 + 1).
Split user input using str.split(), and check whether the resulting list is valid:

1) If the input does not consist of 3 elements, raise a FormulaError, which is a custom Exception.
2) Try to convert the first and third input to a float (like so: float_value = float(str_value));
Catch any ValueError that occurs, and instead raise a FormulaError;
3) If the second input is not '+' or '-', again raise a FormulaError;
4) If the input is valid, perform the calculation and print out the result. The user is then prompted to provide
new input, and so on, until the user enters quit.

Excepted output:
    >> 1 + 1
    2.0
    >> 3.2 - 1.5
    1.7000000000000002
    >> quit
"""


class FormulaError(Exception):
    pass


def parse_input(input_str: str) -> tuple:
    elements = input_str.split()

    if len(elements) != 3:
        raise FormulaError("Need 3 elements")

    try:
        first, second = [float(e) for e in [elements[0], elements[2]]]
    except ValueError:
        raise FormulaError("Not a valid number")

    if elements[1] not in ['+', '-']:
        raise FormulaError("Use + or -")

    return first, elements[1], second


def calculate(term_1: float, op: str, term_2: float) -> float:
    return term_1 + term_2 if op == '+' else term_1 - term_2


def user_input_generator():
    while True:
        user_input = input(">> ")
        if user_input.lower() == "small":
            break
        yield user_input


for expression in user_input_generator():
    try:
        first, operation, second = parse_input(expression)
        result = calculate(first, operation, second)
        print(result)
    except FormulaError as e:
        print(f"Error: {e}")


"""
2. Take the list of dictionaries we created from the Iris flower data set and write it to a new file in CSV
(comma-separated values) format.

Excepted file content:
    5.1,3.5,1.4,0.2,Iris-setosa
    4.9,3,1.4,0.2,Iris-setosa
    4.7,3.2,1.3,0.2,Iris-setosa
    ...
"""

irises = [
    {'sepal_len': '5.1', 'sepal_width': '3.5', 'petal_len': '1.4', 'petal_width': '0.2', 'species': 'Iris-setosa'},
    {'sepal_len': '4.9', 'sepal_width': '3', 'petal_len': '1.4', 'petal_width': '0.2', 'species': 'Iris-setosa'},
    {'sepal_len': '4.7', 'sepal_width': '3.2', 'petal_len': '1.3', 'petal_width': '0.2', 'species': 'Iris-setosa'},
    {'sepal_len': '4.6', 'sepal_width': '3.1', 'petal_len': '1.5', 'petal_width': '0.2', 'species': 'Iris-setosa'},
    {'sepal_len': '5', 'sepal_width': '3.6', 'petal_len': '1.4', 'petal_width': '0.2', 'species': 'Iris-setosa'},
    {'sepal_len': '7', 'sepal_width': '3.2', 'petal_len': '4.7', 'petal_width': '1.4', 'species': 'Iris-versicolor'},
    {'sepal_len': '6.4', 'sepal_width': '3.2', 'petal_len': '4.5', 'petal_width': '1.5', 'species': 'Iris-versicolor'},
    {'sepal_len': '6.9', 'sepal_width': '3.1', 'petal_len': '4.9', 'petal_width': '1.5', 'species': 'Iris-versicolor'},
    {'sepal_len': '5.5', 'sepal_width': '2.3', 'petal_len': '4', 'petal_width': '1.3', 'species': 'Iris-versicolor'},
    {'sepal_len': '6.5', 'sepal_width': '2.8', 'petal_len': '4.6', 'petal_width': '1.5', 'species': 'Iris-versicolor'},
    {'sepal_len': '6.3', 'sepal_width': '3.3', 'petal_len': '6', 'petal_width': '2.5', 'species': 'Iris-virginica'},
    {'sepal_len': '5.8', 'sepal_width': '2.7', 'petal_len': '5.1', 'petal_width': '1.9', 'species': 'Iris-virginica'},
    {'sepal_len': '7.1', 'sepal_width': '3', 'petal_len': '5.9', 'petal_width': '2.1', 'species': 'Iris-virginica'},
    {'sepal_len': '6.3', 'sepal_width': '2.9', 'petal_len': '5.6', 'petal_width': '1.8', 'species': 'Iris-virginica'},
    {'sepal_len': '6.5', 'sepal_width': '3', 'petal_len': '5.8', 'petal_width': '2.2', 'species': 'Iris-virginica'}
]

csv_lines = [f"{iris['sepal_len']},{iris['sepal_width']},{iris['petal_len']},{iris['petal_width']},{iris['species']}" for iris in irises]


with open('irises.csv', 'w', encoding='utf-8') as f:
    f.writelines(line + '\n' for line in csv_lines)


"""
3. Write a regular expression to validate a phone number in Ukrainian format.
Rules:
    - the number can start with +38, this construction is optional;
    - the number must contain 10 digits from 0 to 9 (excluding +38 construction);
    - 10-digit number must start with 0.
Suitable patterns:
    +380*********
    0*********

Excepted output:
    True
    True
    False
    False
"""

import re

pattern = r'^(\+38)?0\d{9}$'

test_numbers = ['0967898008', '+380967898008', '+38967898008', '+3809678988']

for num in test_numbers:
    print(re.fullmatch(pattern, num) is not None)

print(re.fullmatch(pattern, '0967898008') is not None)
print(re.fullmatch(pattern, '+380967898008') is not None)
print(re.fullmatch(pattern, '+38967898008') is not None)
print(re.fullmatch(pattern, '+3809678988') is not None)
