def bubble_sort(items):
    arr = items.copy()
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # no swaps means the list is already sorted
        if not swapped:
            break

    return arr


def selection_sort(items):
    arr = items.copy()

    for i in range(len(arr)):
        min_index = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


def insertion_sort(items):
    arr = items.copy()

    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > current:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current

    return arr


if __name__ == "__main__":
    data = [64, 25, 12, 22, 11]
    print("Original:       ", data)
    print("Bubble sort:    ", bubble_sort(data))
    print("Selection sort: ", selection_sort(data))
    print("Insertion sort: ", insertion_sort(data))
    print("Built-in sorted:", sorted(data))
