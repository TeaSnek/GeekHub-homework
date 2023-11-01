"""
Write a script that will run through a list of tuples and replace the last
value for each tuple. The list of tuples can be hardcoded. The "replacement"
value is entered by user. The number of elements in the tuples must be
different.
"""

TUPLES_LIST = [('',), ('', '',), ('', '', '',),]


if __name__ == '__main__':
    mutated_list = []
    print('Starting list of tuples: ', TUPLES_LIST)
    for item in TUPLES_LIST:
        replacement = input('Input replacement: ')
        mutated_list.append(item[:-1] + (replacement,))
    
    print('Result: ', mutated_list)
