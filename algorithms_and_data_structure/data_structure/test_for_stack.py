import pytest
from data_structures import Stack


def test_stack_push_peek():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.peek() == 3


def test_stack_pop():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.peek() == 1


def test_stack_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()