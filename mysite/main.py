import time
from bisect import bisect_left


n = 20000000
arr = list(range(n))
target = n//2


s = time.perf_counter_ns()
idx = arr.index(target)
e = time.perf_counter_ns()
print(f"{idx}, {e-s}nanosec")






s = time.perf_counter_ns()
idx = bisect_left(arr, target)
e = time.perf_counter_ns()
print(f"{idx}, {e-s}nanosec")




