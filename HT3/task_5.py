prompt = """
Write a script to remove values duplicates from dictionary. Feel free to
hardcode your dictionary.
"""

test_dict = {
    'name': 'Alice',
    'age': 28,
    'city': 'New York',
    'country': 'USA',
    'occupation': 'Software Developer',
    'hobby': 'Reading',
    'favorite_color': 'Blue',
    'duplicate_value': 'Python',
    'another_duplicate': 'Python'
}


if __name__ == '__main__':
    print('TASK 5:', prompt)
    print('Starting dict:', test_dict, sep='\n')
    buffer = {}
    for key, value in test_dict.items():
        if value not in buffer.values():
            buffer[key] = value
    test_dict = buffer.copy()
    print('Result: ', test_dict)
