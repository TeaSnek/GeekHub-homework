"""
Write a script to get the maximum and minimum value in a dictionary.
"""

import numbers


test_dict = {
    'name': 'Alice',
    'age': 28,
    'city': 'New York',
    'country': 'USA',
    'occupation': 'Software Developer',
    'hobby': 'Reading',
    'favorite_color': 'Blue',
    'duplicate_value': 'Python',
    'another_duplicate': 'Python',
    'max': 5239,
    'min': -3368.6565
}


def only_numeric_sort_higher(x):
    if isinstance(x, numbers.Number):
        return x
    else:
        return float('-inf')


def only_numeric_sort_lower(x):
    if isinstance(x, numbers.Number):
        return x
    else:
        return float('inf')


if __name__ == '__main__':
    print('Starting dict: ', test_dict, sep='\n')
    max_result = max(test_dict.values(), key=only_numeric_sort_higher)
    min_result = min(test_dict.values(), key=only_numeric_sort_lower)
    print(f'Result: min {min_result} | max {max_result}')