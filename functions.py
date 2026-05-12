"""
1. You need to write a function that will convert the specified number to the specified number system.
The function takes two arguments as input: a number and a number system.

Expected output:
    B13
    101100010011
"""

from typing import Union


def convert_to(num: int, base: int) -> Union[str, int]:
        digits = "0123456789ABCDEF"
        result = ""

        while num > 0:
            remainder = num % base
            result = digits[remainder] + result
            num = num // base

        return result


print(convert_to(2835, 16))
print(convert_to(2835, 2))


"""
2. You need to write a function of recursion list sum.
The function takes a list as input.

Expected output:
    30
"""


def sum_recursive_list(data: list) -> int:
    total = 0
    for a in data:
        if isinstance(a,list):
            total += sum_recursive_list(a)
        else:
            total += a
    return total




print(sum_recursive_list([1, 2, [3, 4], [5, 6, [2, 3, 4]]]))


"""
3. You need to write a Python program to find the greatest common divisor (gcd) of two integers.
The function takes two integer values as input.

Expected output:
    2
    5
    25
"""


def calculate_gcd(a: int, b: int) -> int:
        if b == 0:
            return a
        return calculate_gcd(b, a % b)


print(calculate_gcd(12, 14))
print(calculate_gcd(15, 25))
print(calculate_gcd(75, 25))


"""
4. You need to write a function that returns the first n rows of Pascal's triangle.
Each number is the two numbers above it added together.
The function takes the number of triangle rows.

Expected output:
    [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1],
        [1, 5, 10, 10, 5, 1],
    ]
"""


def get_pascal_triangle(n: int) -> list:
        triangle = [[1]]

        for i in range(1, n):
            row = [1]

            for j in range(1, i):
                row.append(triangle[i - 1][j - 1] + triangle[i - 1][j])

            row.append(1)
            triangle.append(row)

        return triangle


print(get_pascal_triangle(6))


"""
5. You need to write a program to find whether a given string starts with a given character using Lambda.
The function takes a word and a letter as input.

Expected output:
    True
    False
"""
starts_with = lambda a,b:a.startswith(b)

starts_with = 'Your code'
print(starts_with('Python', 'P'))
print(starts_with('Java', 'P'))


"""
6. You need to write a program to create Fibonacci series upto n using Lambda and reduce. It's a hard task.
The function takes as input the number of Fibonacci numbers to be calculated.

Expected output:
    [0, 1, 1, 2, 3, 5]
"""

from functools import reduce

fib_series = lambda x: reduce(lambda a, _: a + [a[-1] + a[-2]], range(n-2), [0, 1])

print(fib_series(6))


"""
7. You need to write a program to find intersection of two given arrays using Lambda and filter.
You are given two lists, the result will be a list-intersection of the given ones.

Expected output:
    [1, 2, 8, 9]
"""

first = [1, 2, 3, 5, 7, 8, 9, 10]
second = [1, 2, 4, 8, 9]
result = list(filter(lambda x: x in second,first))
print(result)


"""
8. You need write a program to find palindromes in a given list of strings using Lambda and filter.
According Wikipedia - A palindromic number or numeral palindrome is a number that remains the same
when its digits are reversed. Like 16461, for example, it is "symmetrical".

Expected output:
    ['php', 'sagas', 'repaper', 'madam', 'level']
"""

words = ["php", "sagas", "Python", "abcdefg", "Java", "repaper", "madam", "level"]
result = list(filter(lambda x: x == x[::-1],words))
print(result)


"""
9.  You need write a Python program to add three given lists using Python map and lambda.
You are given three lists, the result will be a list with numbers that are the sum of 
the first values of the given lists, the second values, the third...

Expected output:
    [12, 15, 18]
"""

nums_1 = [1, 2, 3]
nums_2 = [4, 5, 6]
nums_3 = [7, 8, 9]
result = list(map(lambda a,b,c: a+b+c,nums_1,nums_2,nums_3))
print(result)


"""
10. You need a program to make a chain of function decorators (bold, italic, underline etc.).
Apply the string formatting that is given as input to the function.

Expected output:
    <b><i><u>Hello world</u></i></b>
"""


def make_bold(func):
    def wrapper():
        return "<b> " + func() + "</b>"
    return wrapper


def make_italic(func):
    def wrapper():
        return "<u>" + func() + "</u>"
    return wrapper


def make_underline(func):
    def wrapper():
        return "<u>" + func() + "</u>"
    return wrapper



@make_bold
@make_italic
@make_underline
def hello():
    return "Hello world"


print(hello())


"""
11. You need to implement a decorator that calculates the execution time of the function.

Expected output:
    sum_linear_progression finished in 0:00:28.791659 (*here is your time)
    500000000500000000
    sum_constant_progression finished in 0:00:00
    500000000500000000
"""

from datetime import datetime

def timeit(func):
    def wrapper(*args):
        start = datetime.now()
        result = func(*args)
        finish = datetime.now()
        print (finish - start)
    return wrapper


# OR


class Timeit:
    # Your code
    pass


@timeit
def sum_linear_progression(n):
    return sum(range(n + 1))


@timeit
def sum_constant_progression(n):
    return n * (n + 1) // 2


print(sum_linear_progression(100_000_000))
print(sum_constant_progression(100_000_000))
