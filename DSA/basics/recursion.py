def factorial(n):
    # base case stops the recursion
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n):
    # simple recursive version, slow for big n -> O(2^n)
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_memo(n, memo=None):
    # same thing but remember answers already calculated -> O(n)
    if memo is None:
        memo = {}
    if n < 2:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def sum_list(items):
    if not items:
        return 0
    return items[0] + sum_list(items[1:])


def reverse_string(text):
    if len(text) <= 1:
        return text
    return reverse_string(text[1:]) + text[0]


if __name__ == "__main__":
    print("5! =", factorial(5))
    print("fib(10) =", fibonacci(10))
    print("fib_memo(50) =", fibonacci_memo(50))
    print("sum [1..5] =", sum_list([1, 2, 3, 4, 5]))
    print("reverse python =", reverse_string("python"))
