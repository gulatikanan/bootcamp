# List vs Generator: Compare memory usage of [x for x in range(1000000)] vs (x for x in range(1000000)).

import sys
lst = [x for x in range(1000000)]
gen = (x for x in range(1000000))
print(sys.getsizeof(lst))  # large
print(sys.getsizeof(gen))  # small
