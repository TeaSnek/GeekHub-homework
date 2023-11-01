"""
Write a script that combines three dictionaries by updating the first one.
"""


dict_1 = {'foo': 'bar', 'bar': 'buz'}
dict_2 = {'dou': 'jones', 'USD': 36}
dict_3 = {'AUD': 19.2, 'name': 'Tom'}


if __name__ == '__main__':
    print('Starting dicts:', dict_1, dict_2, dict_3, sep='\n')
    dict_1.update(dict_2)
    dict_1.update(dict_3)
    print('Resulting dicts:', dict_1, dict_2, dict_3, sep='\n')
