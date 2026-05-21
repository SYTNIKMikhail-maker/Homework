import pytest
from data_structures import LinkedList


def test_linked_list_append():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.to_list() == [1, 2, 3]


def test_linked_list_prepend():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.prepend(0)
    assert ll.to_list() == [0, 1, 2]


def test_linked_list_lookup():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.lookup(2) == 1
    assert ll.lookup(99) == -1


def test_linked_list_insert():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.insert(1, 99)
    assert ll.to_list() == [1, 99, 2, 3]


def test_linked_list_delete():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.delete(1)
    assert ll.to_list() == [1, 3]
    ll.delete(0)
    assert ll.to_list() == [3]