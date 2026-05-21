from data_structures import HashTable


def test_hash_table_insert_lookup():
    ht = HashTable()
    ht.insert("name", "Misha")
    ht.insert("age", 22)
    assert ht.lookup("name") == "Misha"
    assert ht.lookup("age") == 22
    assert ht.lookup("missing") is None


def test_hash_table_delete():
    ht = HashTable()
    ht.insert("name", "Misha")
    ht.delete("name")
    assert ht.lookup("name") is None