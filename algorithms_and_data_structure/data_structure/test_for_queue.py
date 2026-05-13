from algorithms_and_data_structure.data_structure.data_structures import Queue


def test_queue():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert q.peek() == 1
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.peek() == 3
    print("Queue is normal")


test_queue()