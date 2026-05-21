from data_structures import BinarySearchTree


def test_bst_insert_lookup():
    bst = BinarySearchTree()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(1)
    bst.insert(4)
    assert bst.lookup(3).value == 3
    assert bst.lookup(99) is None


def test_bst_delete():
    bst = BinarySearchTree()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(1)
    bst.insert(4)
    bst.delete(3)
    assert bst.lookup(3) is None
    assert bst.lookup(4).value == 4