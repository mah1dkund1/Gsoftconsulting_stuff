# small array / list practice problems


def find_max(items):
    # doing it manually instead of using max()
    if not items:
        return None
    biggest = items[0]
    for value in items:
        if value > biggest:
            biggest = value
    return biggest


def reverse_list(items):
    # two pointer approach, swap from both ends
    arr = items.copy()
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr


def remove_duplicates(items):
    # set to remember what we have seen, list to keep the order
    seen = set()
    result = []
    for value in items:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def two_sum(nums, target):
    # dict stores value -> index so we get O(n) instead of O(n^2)
    seen = {}
    for index, num in enumerate(nums):
        needed = target - num
        if needed in seen:
            return (seen[needed], index)
        seen[num] = index
    return None


def count_chars(text):
    counts = {}
    for char in text:
        counts[char] = counts.get(char, 0) + 1
    return counts


if __name__ == "__main__":
    print("Max:", find_max([3, 8, 1, 9, 4]))
    print("Reversed:", reverse_list([1, 2, 3, 4, 5]))
    print("No duplicates:", remove_duplicates([1, 2, 2, 3, 1, 4]))
    print("Two sum (target 9):", two_sum([2, 7, 11, 15], 9))
    print("Char counts:", count_chars("hello"))
