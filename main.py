import time
import heapq
import random
import csv

# Generate 5 types of input arrays
random_arrays = {
    "losowe": [random.randint(-100, 100) for _ in range(300)],
    "rosnące": sorted([random.randint(-100, 100) for _ in range(300)]),
    "malejące": sorted([random.randint(-100, 100) for _ in range(300)], reverse=True),
    "stałe": [42 for _ in range(300)],
    "v_ształtny": sorted([random.randint(-100, 0) for _ in range(150)], reverse=True) + sorted([random.randint(0, 100) for _ in range(150)])
}

def record_progress(progress, array_type, step, start):
    if step <= 300 and step % 15 == 0:
        if step not in progress:
            progress[step] = {}
        progress[step][array_type] = time.perf_counter() - start

def finalize_progress(progress, array_type, start):
    if 300 not in progress or array_type not in progress.get(300, {}):
        record_progress(progress, array_type, 300, start)

def insertion_sort(arr, array_type, progress):
    a = arr[:]
    start = time.perf_counter()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
        if i % 15 == 0:
            record_progress(progress, array_type, i, start)
    finalize_progress(progress, array_type, start)
    return a, time.perf_counter() - start

def selection_sort(arr, array_type, progress):
    a = arr[:]
    start = time.perf_counter()
    for i in range(len(a)):
        min_idx = min(range(i, len(a)), key=a.__getitem__)
        a[i], a[min_idx] = a[min_idx], a[i]
        if i % 15 == 0 and i != 0:
            record_progress(progress, array_type, i, start)
    finalize_progress(progress, array_type, start)
    return a, time.perf_counter() - start

def heap_sort(arr, array_type, progress):
    a = arr[:]
    start = time.perf_counter()
    heapq.heapify(a)
    out = []
    for i in range(len(a)):
        out.append(heapq.heappop(a))
        if (i+1) % 15 == 0:
            record_progress(progress, array_type, i+1, start)
    finalize_progress(progress, array_type, start)
    return out, time.perf_counter() - start

def merge_sort(arr, array_type, progress):
    a = arr[:]
    start = time.perf_counter()
    steps = [i for i in range(15, 301, 15)]
    logged = set()
    count = 0

    def _merge_sort(a):
        nonlocal count
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        l = _merge_sort(a[:mid])
        r = _merge_sort(a[mid:])
        merged = merge(l, r)
        count += len(merged)
        for s in steps:
            if s not in logged and count >= s:
                record_progress(progress, array_type, s, start)
                logged.add(s)
            elif s > count:
                break
        return merged

    sorted_arr = _merge_sort(a)
    finalize_progress(progress, array_type, start)
    return sorted_arr, time.perf_counter() - start

def merge(l, r):
    res = []
    i = j = 0
    while i < len(l) and j < len(r):
        if l[i] < r[j]: res.append(l[i]); i += 1
        else: res.append(r[j]); j += 1
    return res + l[i:] + r[j:]

def test_all_sorts():
    sort_funcs = {
        "insertion_sort": insertion_sort,
        "selection_sort": selection_sort,
        "heap_sort": heap_sort,
        "merge_sort": merge_sort
    }

    for name, func in sort_funcs.items():
        print(f"\n{name}:")
        progress = {}
        for arr_name, arr in random_arrays.items():
            print(f"{arr_name}:")
            _, total = func(arr, arr_name, progress)
            print(f"total: {total:.6f}s\n")

        steps = sorted(progress)
        headers = ["Numer"] + list(random_arrays)
        rows = [[s] + [f"{progress[s].get(t, ''):.6f}" if t in progress[s] else '' for t in random_arrays] for s in steps]
        with open(f"{name}_table.csv", 'w', newline='') as f:
            csv.writer(f).writerows([headers] + rows)

if __name__ == "__main__":
    test_all_sorts()
