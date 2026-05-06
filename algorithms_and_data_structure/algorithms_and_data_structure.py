class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def prepend(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self.length += 1

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.length += 1
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        self.length += 1

    def lookup(self, value):
        current = self.head
        index = 0
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def insert(self, index, value):
        if index < 0 or index > self.length:
            raise IndexError("Index out of range")
        if index == 0:
            self.prepend(value)
            return
        new_node = Node(value)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self.length += 1

    def delete(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        if index == 0:
            self.head = self.head.next
            self.length -= 1
            return
        current = self.head
        for _ in range(index - 1):
            current = current.next
        current.next = current.next.next
        self.length -= 1

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def enqueue(self, value):
        new_node = Node(value)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def dequeue(self):
        if self.head is None:
            raise IndexError("Queue is empty")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.length -= 1
        return value

    def peek(self):
        if self.head is None:
            raise IndexError("Queue is empty")
        return self.head.value


class Stack:
    def __init__(self):
        self.top = None
        self.length = 0

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node
        self.length += 1

    def pop(self):
        if self.top is None:
            raise IndexError("Stack is empty")
        value = self.top.value
        self.top = self.top.next
        self.length -= 1
        return value

    def peek(self):
        if self.top is None:
            raise IndexError("Stack is empty")
        return self.top.value


class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = BSTNode(value)
        if self.root is None:
            self.root = new_node
            return
        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right

    def lookup(self, value):
        current = self.root
        while current:
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return None

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            min_node = node.right
            while min_node.left:
                min_node = min_node.left
            node.value = min_node.value
            node.right = self._delete(node.right, min_node.value)
        return node


class HashTable:
    def __init__(self):
        self.size = 10
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])

    def lookup(self, key):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None

    def delete(self, key):
        index = self._hash(key)
        self.table[index] = [p for p in self.table[index] if p[0] != key]


class GraphNode:
    def __init__(self, value):
        self.value = value
        self.neighbors = []


class Graph:
    def __init__(self):
        self.nodes = []

    def insert(self, value, neighbors=None):
        new_node = GraphNode(value)
        self.nodes.append(new_node)
        if neighbors:
            for neighbor in neighbors:
                new_node.neighbors.append(neighbor)
                neighbor.neighbors.append(new_node)
        return new_node

    def lookup(self, value):
        for node in self.nodes:
            if node.value == value:
                return node
        return None

    def delete(self, node):
        for neighbor in node.neighbors:
            neighbor.neighbors.remove(node)
        self.nodes.remove(node)


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


def test_bst():
    bst = BinarySearchTree()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(1)
    bst.insert(4)
    assert bst.lookup(3).value == 3
    assert bst.lookup(99) is None
    bst.delete(3)
    assert bst.lookup(3) is None
    assert bst.lookup(4).value == 4
    print("BST is normal")


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


test_linked_list()
test_queue()
test_stack()
test_bst()
test_hash_table()
test_graph()
print("All tests were passed")