from algorithms_and_data_structure.data_structure.data_structures import LinkedList


def test_linked_list():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.to_list() == [1, 2, 3]
    ll.prepend(0)
    assert ll.to_list() == [0, 1, 2, 3]
    assert ll.lookup(2) == 2
    assert ll.lookup(99) == -1
    ll.insert(2, 99)
    assert ll.to_list() == [0, 1, 99, 2, 3]
    ll.delete(2)
    assert ll.to_list() == [0, 1, 2, 3]
    ll.delete(0)
    assert ll.to_list() == [1, 2, 3]
    print("LinkedList is normal")


test_linked_list()