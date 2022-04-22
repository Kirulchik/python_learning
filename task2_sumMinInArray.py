array = [34, 55, 2, 787, 364, 45, 5, 6]
def sum_min_element (arr):
    min = arr[0]
    min2 = arr[0]

    for element in arr:
        if element < min:
            min = min2
            min2 = element
    return min + min2

print( sum_min_element(array) )