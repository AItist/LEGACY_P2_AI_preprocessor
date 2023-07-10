
import concurrent.futures

# a simple function that takes a number and returns its square
def square(n):
    for i in range(3):
        print(f'{n}:{i} ')
    return n

# create a ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # The numbers that we want to get the square of
    numbers = [2, 3, 4, 5, 6]

    # Submit tasks for execution
    futures = [executor.submit(square, num) for num in numbers]

    # Collect and print the results as they become available
    for future in concurrent.futures.as_completed(futures):
        print(f'x:{future.result()}')
