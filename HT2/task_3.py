# Write a script which accepts a <number> from user and print out a sum of the
# first <number> positive integers.


if __name__ == '__main__':
    print(sum([x+1 for x in range(int(input()))]))