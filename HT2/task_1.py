# Write a script which accepts a sequence of comma-separated numbers from user
# and generate a list and a tuple with those numbers.


if __name__ == '__main__':
    line = input()
    lst = list(map(int, line.split(',')))
    tpl = tuple(lst)
    print(lst, tpl, sep='\n')
