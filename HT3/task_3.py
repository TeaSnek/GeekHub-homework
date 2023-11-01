"""
Write a script to concatenate following dictionaries to create a new one.
dict_1 = {'foo': 'bar', 'bar': 'buz'}
dict_2 = {'dou': 'jones', 'USD': 36}
dict_3 = {'AUD': 19.2, 'name': 'Tom'}
"""

dict_1 = {'foo': 'bar', 'bar': 'buz'}
dict_2 = {'dou': 'jones', 'USD': 36}
dict_3 = {'AUD': 19.2, 'name': 'Tom'}


if __name__ == '__main__':
    resulting_dict = dict(dict_1, **dict_2)
    resulting_dict.update(dict_3) 
    print('Resulting dict:', resulting_dict, sep='\n')

# according to
# https://stackoverflow.com/questions/1781571/how-to-concatenate-two-dictionaries-to-create-a-new-one
# this is the fastest approach to do so
