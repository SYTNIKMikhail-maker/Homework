from algorithms_and_data_structure.data_structure.data_structures import Stack


def test_stack():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.peek() == 3
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.peek() == 1
    print("Stack is normal")


test_stack()