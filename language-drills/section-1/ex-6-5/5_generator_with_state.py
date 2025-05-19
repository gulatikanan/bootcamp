from typing import Iterator

def running_total(numbers: list[int]) -> Iterator[int]:
    total = 0
    for num in numbers:
        total += num
        yield total

for total in running_total([1, 2, 3, 4]):
    print(total)