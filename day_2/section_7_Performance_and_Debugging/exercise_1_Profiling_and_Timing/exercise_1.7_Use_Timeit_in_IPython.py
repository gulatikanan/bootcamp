"""
Use Timeit in IPython

Instructions:
Complete the exercise according to the requirements.
"""
import timeit

# Example: time sum(range(10000))
execution_time = timeit.timeit("sum(range(10000))", number=100)
print(f"Average time over 100 runs: {execution_time / 100:.6f} seconds")


#Install ipython3 using the command - sudo apt install ipython3
#then launch it with 'ipython3' command in the terminal
#from the terminal run - %timeit sum(range(10000))
