#!/usr/bin/env python3.10

"""
30 / 4 = 7.5
30 // 4 = 7

rank 0 -> 0, 7
rank 1 -> 7, 14
rank 2 -> 14, 21
rank 3 -> 21, 30
"""

def get_work(work_count, num_workers, rank):
    if num_workers > work_count or rank >= num_workers:
        raise Exception(f"Bad input: {work_count=} {num_workers=} {rank=}")
    slice_size = work_count // num_workers
    start = rank * slice_size
    end = (rank + 1) * slice_size if rank < num_workers - 1 else work_count
    return start, end - 1

def run_coverage_test(work_count):
    def run_test(num_workers):
        work = [0] * work_count
        for rank in range(0, num_workers):
            print(f"  Test: {work_count=} {num_workers=} {rank=}")
            l, r = get_work(work_count, num_workers, rank)
            for i in range(l, r + 1):
                work[i] += 1
        for act in work:
            if act != 1:
                raise Exception(f"Malfunction for {work_count=} {num_workers=} {rank=}")
    for i in range(1, work_count + 1):
        run_test(i)

for i in range(1, 100 + 1):
    print(f"Running test for work_count {i}")
    run_coverage_test(i)
