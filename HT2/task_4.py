# Write a script which accepts a <number> from user and then <number> times
# asks user for string input. At the end script must print out result of
# concatenating all <number> strings.


if __name__ == '__main__':
    input_counter = int(input('input target a <number> of lines: '))
    print(*[input('input smth: ') for _ in range(input_counter)], sep='')
