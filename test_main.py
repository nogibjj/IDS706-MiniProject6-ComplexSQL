"""
Test goes here

"""

from main import add, subtract, multiply, divide


def test_add():
    assert add(1, 2) == 3

def test_subtract():
    assert subtract(1, 2) == -1

def test_multiply():
    assert multiply(1, 2) == 2

def test_divide():
    assert divide(2, 1) == 2

if __name__ == "__main__":
    test_add()
    test_subtract()
    test_multiply()
    test_divide()
    print("Everything passed")