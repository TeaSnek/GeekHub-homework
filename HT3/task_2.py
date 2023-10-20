prompt = """
Write a script to remove an empty elements from a list.

Test list: [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]
"""

test_list = [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {},
              ['d', 'a', 'y'], '', []]


if __name__ == '__main__':
    print('TASK 2:', prompt)
    i = 0
    while i < len(test_list):
        if not test_list[i]:
            test_list.pop(i)
        else:
            i += 1

    print('Result:', test_list)
