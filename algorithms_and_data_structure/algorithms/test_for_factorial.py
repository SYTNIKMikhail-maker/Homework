from algorithms import factorial


def test_factorial():
    # Test factorial with various inputs.
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(10) == 3628800
    print("Factorial is normal")


test_factorial()