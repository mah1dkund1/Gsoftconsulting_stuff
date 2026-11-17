from collections import deque


class Stack:
    # LIFO - last in, first out. A python list works fine as a stack

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


class Queue:
    # FIFO - first in, first out. deque is used because list.pop(0) is O(n)

    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.items.popleft()

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


def is_balanced(expression):
    # classic stack problem: check if brackets are balanced
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = Stack()

    for char in expression:
        if char in "([{":
            stack.push(char)
        elif char in ")]}":
            if stack.pop() != pairs[char]:
                return False

    return stack.is_empty()


if __name__ == "__main__":
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    print("Stack pop:", s.pop())
    print("Stack peek:", s.peek())

    q = Queue()
    q.enqueue("a")
    q.enqueue("b")
    q.enqueue("c")
    print("Queue dequeue:", q.dequeue())
    print("Queue size:", q.size())

    print("(a[b]{c}) balanced?", is_balanced("(a[b]{c})"))
    print("(] balanced?", is_balanced("(]"))
