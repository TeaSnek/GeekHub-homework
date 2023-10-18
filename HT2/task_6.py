'''Write a script to check whether a value from user input is contained in a group of values.

    e.g. [1, 2, 'u', 'a', 4, True] --> 2 --> True
         [1, 2, 'u', 'a', 4, True] --> 5 --> False'''

TARGET_GROUP = [1, 2, 'u', 'a', 4, True]


if __name__ == '__main__':
    user_input = input()
    if user_input in ['True', 'False']:
        print(bool(user_input) in TARGET_GROUP)
    elif user_input.isdecimal():
        print(int(user_input) in TARGET_GROUP)
    else:
        print(user_input in TARGET_GROUP)
