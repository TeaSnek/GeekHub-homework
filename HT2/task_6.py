'''Write a script to check whether a value from user input is contained in a group of values.

    e.g. [1, 2, 'u', 'a', 4, True] --> 2 --> True
         [1, 2, 'u', 'a', 4, True] --> 5 --> False'''

TARGET_GROUP = [1, 2, 'u', 'a', 4, True]


if __name__ == '__main__':
    user_input = input()
    try:
        match user_input:
            case 'True':
                print(True in TARGET_GROUP)
            case 'False':
                print(False in TARGET_GROUP)
            case _:
                print(int(user_input) in TARGET_GROUP)
    except ValueError:
        print(user_input in TARGET_GROUP)