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
    separate = input_str.split()
    if len(separate) != 3:
        raise FormulaError("Input must consist of 3 elements")
    try:
        first = float(separate[0])
        second = float(separate[2])
    except:
        raise FormulaError ("First and third elements must be numbers")
    if separate[1] is not "+" or "-":
        raise FormulaError ("Operator must be + or -")
    return first,separate[1],second






def calculate(term_1: float, op: str, term_2: float) -> float:
    if op == '+':
        return term_1 + term_2
    if op == '-':
        return term_1 - term_2





while True:
    user_input = input("Input something pls ->> ")

    if user_input == 'quit':
        break
    try:
        first,operation,second,  = parse_input(user_input)
        result = calculate(first, operation, second)
        print(result)
    except FormulaError as e:
        print(e)



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

with open('iris.csv','w',encoding = 'utf-8') as f:
    for i in irises:
        f.write(",".join(i.values()) + '/n')



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

pattern = r'(\+38)?0\d{9}'

print(re.fullmatch(pattern, '0967898008') is not None)
print(re.fullmatch(pattern, '+380967898008') is not None)
print(re.fullmatch(pattern, '+38967898008') is not None)
print(re.fullmatch(pattern, '+3809678988') is not None)
