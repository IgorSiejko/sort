import time
import heapq
import random
import csv

# Generate 5 specific arrays for testing
random_arrays = {
    "random": [random.randint(-100, 100) for _ in range(300)],
    "ascending": sorted([random.randint(-100, 100) for _ in range(300)]),
    "descending": sorted([random.randint(-100, 100) for _ in range(300)], reverse=True),
    "constant": [42 for _ in range(300)],
    "v-shaped": sorted([random.randint(-100, 0) for _ in range(150)], reverse=True) + sorted([random.randint(0, 100) for _ in range(150)])
}

# Save progress list to CSV
def save_progress_to_csv(progress_list, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Step", "Time (seconds)"])
        writer.writerows(progress_list)

# Insertion Sort with step time tracking
def insertion_sort(arr, filename):
    array = arr.copy()
    progress = []
    start = time.perf_counter()
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
        if i % 15 == 0:
            mid_time = time.perf_counter()
            progress.append((i, mid_time - start))
    end = time.perf_counter()
    save_progress_to_csv(progress, filename)
    return array, end - start

# Selection Sort with step time tracking
def selection_sort(arr, filename):
    array = arr.copy()
    progress = []
    start = time.perf_counter()
    n = len(array)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if array[j] < array[min_idx]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
        if i % 15 == 0 and i != 0:
            mid_time = time.perf_counter()
            progress.append((i, mid_time - start))
    end = time.perf_counter()
    save_progress_to_csv(progress, filename)
    return array, end - start

# Heap Sort with step time tracking
def heap_sort(arr, filename):
    array = arr.copy()
    progress = []
    start = time.perf_counter()
    heapq.heapify(array)
    sorted_array = []
    for i in range(len(array)):
        sorted_array.append(heapq.heappop(array))
        if (i+1) % 15 == 0:
            mid_time = time.perf_counter()
            progress.append((i+1, mid_time - start))
    end = time.perf_counter()
    save_progress_to_csv(progress, filename)
    return sorted_array, end - start

# Merge Sort with step time tracking

def merge_sort(arr, filename):
    array = arr.copy()
    progress = []
    start = time.perf_counter()
    operation_count = 0

    def _merge_sort_recursive(array):
        nonlocal start, progress, operation_count
        if len(array) <= 1:
            return array
        mid = len(array) // 2
        left = _merge_sort_recursive(array[:mid])
        right = _merge_sort_recursive(array[mid:])
        merged = _merge(left, right)
        prev_count = operation_count
        operation_count += len(merged)
        if operation_count // 15 > prev_count // 15:
            mid_time = time.perf_counter()
            progress.append((operation_count, mid_time - start))
        return merged

    sorted_array = _merge_sort_recursive(array)
    end = time.perf_counter()
    save_progress_to_csv(progress, filename)
    return sorted_array, end - start

# Merge helper function

def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Main test function for sorting algorithms

def test_all_sorts():
    sort_functions = {
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Heap Sort": heap_sort,
        "Merge Sort": merge_sort
    }

    # Print arrays before sorting
    print("Generated arrays:")
    for name, array in random_arrays.items():
        print(f"{name}: {array}")

    # Run and print results of sorting
    print("\nSorting results:")
    for sort_name, sort_func in sort_functions.items():
        print(f"\n{sort_name}:")
        for array_name, array in random_arrays.items():
            print(f"{array_name}:")
            filename = f"{sort_name.replace(' ', '_')}_{array_name}.csv"
            _, duration = sort_func(array, filename)
            print(f"Total time: {duration:.6f} seconds\n")

# Run the tests
if __name__ == "__main__":
    test_all_sorts()
