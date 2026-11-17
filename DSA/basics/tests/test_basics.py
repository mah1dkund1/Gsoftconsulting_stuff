from searching import linear_search, binary_search
from sorting import bubble_sort, selection_sort, insertion_sort
from stack_and_queue import Stack, Queue, is_balanced
from recursion import factorial, fibonacci, fibonacci_memo, sum_list, reverse_string
from list_problems import find_max, reverse_list, remove_duplicates, two_sum, count_chars


def test_searching():
    assert linear_search([4, 2, 9], 9) == 2
    assert linear_search([4, 2, 9], 5) == -1
    assert binary_search([1, 3, 5, 7, 9], 7) == 3
    assert binary_search([1, 3, 5, 7, 9], 4) == -1
    assert binary_search([], 1) == -1


def test_sorting():
    data = [5, 2, 9, 1, 5, 6]
    expected = [1, 2, 5, 5, 6, 9]
    assert bubble_sort(data) == expected
    assert selection_sort(data) == expected
    assert insertion_sort(data) == expected
    # original list should not be changed
    assert data == [5, 2, 9, 1, 5, 6]


def test_stack():
    s = Stack()
    assert s.pop() is None
    s.push(1)
    s.push(2)
    assert s.peek() == 2
    assert s.pop() == 2
    assert s.size() == 1


def test_queue():
    q = Queue()
    assert q.dequeue() is None
    q.enqueue("a")
    q.enqueue("b")
    assert q.dequeue() == "a"
    assert q.size() == 1


def test_is_balanced():
    assert is_balanced("(a[b]{c})")
    assert not is_balanced("(]")
    assert not is_balanced("((")


def test_recursion():
    assert factorial(5) == 120
    assert factorial(0) == 1
    assert fibonacci(10) == 55
    assert fibonacci_memo(50) == 12586269025
    assert sum_list([1, 2, 3]) == 6
    assert reverse_string("abc") == "cba"


def test_list_problems():
    assert find_max([3, 8, 1]) == 8
    assert find_max([]) is None
    assert reverse_list([1, 2, 3]) == [3, 2, 1]
    assert remove_duplicates([1, 2, 2, 3, 1]) == [1, 2, 3]
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert count_chars("aab") == {"a": 2, "b": 1}
