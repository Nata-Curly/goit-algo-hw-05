def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        mid = (left + right) // 2
        iterations += 1

        if arr[mid] == target:
            return iterations, arr[mid]
        elif arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1

    return iterations, upper_bound


arr = [0.1, 0.5, 1.2, 1.7, 2.5, 3.0, 3.6, 4.1, 4.8]
target = 4.0

print("Кількість ітерацій та верхня межа:", binary_search(arr, target))
