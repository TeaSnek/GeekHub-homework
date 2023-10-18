# Write a script which accepts a <number> from user and print out a sum of the
# first <number> positive integers.


if __name__ == '__main__':
    number = int(input('Input a <number>: '))
    print(sum([x + 1 for x in range(number)]))