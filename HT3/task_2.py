"""
Write a script to remove an empty elements from a list.

Test list: [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]
"""

test_list = [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {},
              ['d', 'a', 'y'], '', []]


if __name__ == '__main__':
    print('Result:', [item for item in test_list if item])
