"""
1. MyEnumerate - iterate characters with index
"""

class MyEnumerate:
    def __init__(self, data: str):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        result = (self.index, self.data[self.index])
        self.index += 1
        return result


for index, letter in MyEnumerate('abcdf'):
    print(f'{index} : {letter}')


"""
2. CircleIterator and Circle - loop through chars up to max_times
"""

class CircleIterator:
    def __init__(self, data: str, max_times: int):
        self.data = data
        self.max_times = max_times
        self.count = 0

    def __next__(self):
        if self.count >= self.max_times:
            raise StopIteration
        result = self.data[self.count % len(self.data)]
        self.count += 1
        return result


class Circle:
    def __init__(self, data: str, max_times: int):
        self.data = data
        self.max_times = max_times

    def __iter__(self):
        return CircleIterator(self.data, self.max_times)


c = Circle('abc', 5)
print(list(c))


"""
3. Generator of prime numbers up to limit
"""

def gen_primes(limit: int):
    for num in range(2, limit + 1):
        if all(num % i != 0 for i in range(2, num)):
            yield num


for i in gen_primes(10):
    print(i, end=' ')
print()


"""
4. Join numbers 0-14 with commas
"""

numbers = range(15)
result = ','.join(str(n) for n in numbers)
print(result)


"""
5. Extract numbers from string and sum them
"""

numbers = '10 abc 20 de44 30 55fg 40'
total = sum(int(x) for x in numbers.split() if x.isdigit())
print(f'Sum: {total}')


"""
6. Swap keys and values in a dictionary
"""

d = {'a': 1, 'b': 2, 'c': 3}
flipped_d = {v: k for k, v in d.items()}
print(flipped_d)
