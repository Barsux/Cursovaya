# Функция пузырьковой сортировки массива, возвращает кортеж типа:
# (Список индексов в отсортированном порядке, Список элементов в отсортированном порядке)
# Опционально принимает анонимную функцию как ключ сортировки
def bubble_sort_idx(array, key=lambda val: val) -> tuple:
    idxs = list(range(len(array)))
    for i in range(len(array)):
        for j in range(len(array)):
            if key(array[i]) < key(array[j]):
                array[i], array[j] = array[j], array[i]
                idxs[i], idxs[j] = idxs[j], idxs[i]
    return idxs, array


# Функция находит максимальный индекс в массиве
# Опционально принимает анонимную функцию как ключ для максимального значения
def find_max_idx(array, key=lambda val: val) -> list:
    idxs = [0]
    for i, val in enumerate(array):
        if i == 0:
            continue
        if key(val) > key(array[idxs[0]]):
            idxs = [i]
        elif key(val) == key(array[idxs[0]]):
            idxs.append(i)
    return idxs


# Функция суммирует массив,
# Cделана только для применения вместе с анонимной функцией на замену встроенного sum()
def sum_by_key(array, key=lambda val: val) -> int:
    sum_val = 0
    for val in array:
        sum_val += key(val)
    return sum_val


# Функция бинарного поиска
def binary_search(array, value) -> int:
    left = 0
    right = len(array) - 1
    while left <= right:
        middle = (right + left) // 2
        if array[middle] == value:
            return middle
        elif array[middle] < value:
            left = middle + 1
        else:
            right = middle - 1
    return -1
