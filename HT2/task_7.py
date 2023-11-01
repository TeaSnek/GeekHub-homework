# Write a script to concatenate all elements in a list into a string and print it.
# List must be include both strings and integers and must be hardcoded.

TARGET_LIST = [1, 2, 'u', 'a', 4, 'True']


if __name__ == '__main__':
    print(*TARGET_LIST, sep='')
