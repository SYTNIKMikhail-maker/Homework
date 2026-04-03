"""Calculator module for basic arithmetic operations."""


class Calculator:
    """A simple calculator class."""

    def addition(self, a, b):
        """Return the sum of a and b."""
        return a + b

    def subtraction(self, a, b):
        """Return the difference of a and b."""
        return a - b

    def multiplication(self, a, b):
        """Return the product of a and b."""
        return a * b

    def division(self, a, b):
        """Return the result of dividing a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b
