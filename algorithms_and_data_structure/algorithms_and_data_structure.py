"""Data Structures implementation without using built-in collections.
Includes: LinkedList, Queue, Stack, BinarySearchTree, HashTable, Graph.
"""


class Node:
    """A single node that stores a value and a reference to the next node."""

    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    """A linear data structure where each element points to the next one."""

    def __init__(self):
        self.head = None
        self.length = 0

    def prepend(self, value):
        """Add a new element to the beginning of the list."""
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self.length += 1

    def append(self, value):
        """Add a new element to the end of the list."""
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
        """Return the index of the first element with the given value, or -1 if not found."""
        current = self.head
        index = 0
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def insert(self, index, value):
        """Insert a new element at the given index, shifting elements to the right."""
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
        """Delete the element at the given index."""
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
        """Return all elements as a Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result


class Queue:
    """A FIFO data structure — first element added is the first to be removed."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def enqueue(self, value):
        """Add a new element to the end of the queue."""
        new_node = Node(value)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def dequeue(self):
        """Remove and return the element from the head of the queue."""
        if self.head is None:
            raise IndexError("Queue is empty")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.length -= 1
        return value

    def peek(self):
        """Return the value at the head of the queue without removing it."""
        if self.head is None:
            raise IndexError("Queue is empty")
        return self.head.value


class Stack:
    """A LIFO data structure — last element added is the first to be removed."""

    def __init__(self):
        self.top = None
        self.length = 0

    def push(self, value):
        """Add a new element to the top of the stack."""
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node
        self.length += 1

    def pop(self):
        """Remove and return the element from the top of the stack."""
        if self.top is None:
            raise IndexError("Stack is empty")
        value = self.top.value
        self.top = self.top.next
        self.length -= 1
        return value

    def peek(self):
        """Return the value at the top of the stack without removing it."""
        if self.top is None:
            raise IndexError("Stack is empty")
        return self.top.value


class BSTNode:
    """A single node in a Binary Search Tree with left and right children."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """A tree where left child is always smaller and right child is always larger."""

    def __init__(self):
        self.root = None

    def insert(self, value):
        """Add a new element to the correct position in the tree."""
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
        """Find and return the node with the given value, or None if not found."""
        current = self.root
        while current:
            if value == current.value:
                return current
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return None

    def delete(self, value):
        """Delete the node with the given value from the tree."""
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        """Recursively find and remove the node, keeping the tree valid."""
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
    """A key-value store that uses a hash function to find elements in O(1)."""

    def __init__(self):
        self.size = 10
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        """Convert a key into a table index."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Add or update a key-value pair in the table."""
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])

    def lookup(self, key):
        """Return the value for the given key, or None if not found."""
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None

    def delete(self, key):
        """Remove the key-value pair with the given key."""
        index = self._hash(key)
        self.table[index] = [p for p in self.table[index] if p[0] != key]


class GraphNode:
    """A single node in a graph that stores a value and its neighbors."""

    def __init__(self, value):
        self.value = value
        self.neighbors = []


class Graph:
    """An undirected graph where nodes are connected by edges without weights."""

    def __init__(self):
        self.nodes = []

    def insert(self, value, neighbors=None):
        """Add a new node and connect it to the given neighbors."""
        new_node = GraphNode(value)
        self.nodes.append(new_node)
        if neighbors:
            for neighbor in neighbors:
                new_node.neighbors.append(neighbor)
                neighbor.neighbors.append(new_node)
        return new_node

    def lookup(self, value):
        """Find and return the node with the given value, or None if not found."""
        for node in self.nodes:
            if node.value == value:
                return node
        return None

    def delete(self, node):
        """Remove a node and all its connections from the graph."""
        for neighbor in node.neighbors:
            neighbor.neighbors.remove(node)
        self.nodes.remove(node)


def test_linked_list():
    """Test LinkedList operations."""
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
    """Test Queue operations."""
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
    """Test Stack operations."""
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
    """Test BinarySearchTree operations."""
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
    """Test HashTable operations."""
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
    """Test Graph operations."""
    g = Graph()
    a = g.insert("A")
    b = g.insert("B", [a])
    g.insert("C", [a, b])
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