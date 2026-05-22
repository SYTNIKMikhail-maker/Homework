from data_structures import Graph


def test_graph_insert_lookup():
    g = Graph()
    a = g.insert("A")
    b = g.insert("B", [a])
    g.insert("C", [a, b])
    assert g.lookup("A") == a
    assert b in a.neighbors
    assert a in b.neighbors


def test_graph_delete():
    g = Graph()
    a = g.insert("A")
    b = g.insert("B", [a])
    g.delete(b)
    assert b not in a.neighbors
    assert g.lookup("B") is None