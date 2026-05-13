from algorithms_and_data_structure.data_structure.data_structures import HashTable


def test_hash_table():
    ht = HashTable()
    ht.insert("name", "Misha")
    ht.insert("age", 22)
    assert ht.lookup("name") == "Misha"
    assert ht.lookup("age") == 22
    assert ht.lookup("missing") is None
    ht.delete("name")
    assert ht.lookup("name") is None
    print("HashTable is normal")


test_hash_table()