def my_map_function(function, lst):
    result = []

    for item in lst:
        result.append(function(item))

    return result


def multi(x):
    return x * 2


numbers = [1, 2, 3]
mapped_numbers = my_map_function(multi, numbers)

print(mapped_numbers)
