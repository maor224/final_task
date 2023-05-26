import time
from functools import wraps


def cache_decorator(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Generating a unique key based on function arguments
        key = tuple(args) + tuple(sorted(kwargs.items()))

        if key in cache:
            result = cache[key]
            print("Result retrieved from cache")
        else:
            print("Performing heavy calculations...")
            result = func(*args, **kwargs)

            cache[key] = result
            print("Result cached")

        return result

    return wrapper


# Heavy function with cache decorator
@cache_decorator
def heavy_function(param1, param2):
    time.sleep(3)
    result = param1 + param2
    return result


print(heavy_function(2, 3))
print(heavy_function(2, 3))
print(heavy_function(3, 5))
print(heavy_function(2, 3))
