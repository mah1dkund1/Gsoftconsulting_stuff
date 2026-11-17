def linear_search(items, target):
    # check every element one by one -> O(n)
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1


def binary_search(sorted_items, target):
    # list must be sorted, cut the search space in half each step -> O(log n)
    low = 0
    high = len(sorted_items) - 1

    while low <= high:
        mid = (low + high) // 2
        if sorted_items[mid] == target:
            return mid
        elif sorted_items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


if __name__ == "__main__":
    numbers = [4, 2, 9, 7, 1]
    print("Linear search for 7:", linear_search(numbers, 7))

    sorted_numbers = [1, 3, 5, 7, 9, 11]
    print("Binary search for 9:", binary_search(sorted_numbers, 9))
    print("Binary search for 4:", binary_search(sorted_numbers, 4))
