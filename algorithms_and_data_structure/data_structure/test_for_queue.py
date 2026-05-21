import pytest
from data_structures import Queue


def test_queue_enqueue_peek():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert q.peek() == 1


def test_queue_dequeue():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.peek() == 3


def test_queue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()