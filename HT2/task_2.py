# Write a script which accepts two sequences of comma-separated colors from user.
# Then print out a set containing all the colors from color_list_1 which are
# not present in color_list_2.


if __name__ == '__main__':
    x = set(input().split(','))
    y = set(input().split(','))
    print(x, y)
    print(x.difference(y))
