from algorithms_and_data_structure.data_structure.data_structures import Graph


def test_graph():
    g = Graph()
    a = g.insert("A")
    b = g.insert("B", [a])
    c = g.insert("C", [a, b])
    assert g.lookup("A") == a
    assert b in a.neighbors
    assert a in b.neighbors
    g.delete(b)
    assert b not in a.neighbors
    assert g.lookup("B") is None
    print("Graph is normal")


test_graph()