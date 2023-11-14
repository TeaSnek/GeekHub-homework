"""
Написати функцію, яка приймає два параметри: ім'я (шлях) файлу та кількість
символів. Файл також додайте в репозиторій. На екран повинен вивестись список
із трьома блоками - символи з початку, із середини та з кінця файлу. Кількість
символів в блоках - та, яка введена в другому параметрі. Придумайте самі, як
обробляти помилку, наприклад, коли кількість символів більша, ніж є в файлі
або, наприклад, файл із двох символів і треба вивести по одному символу, то що
виводити на місці середнього блоку символів?). Не забудьте додати перевірку чи
файл існує.
"""
import os


def extractor(filename, symbols_amount):
    full_path = os.path.join(os.getcwd(), filename)
    print(full_path)
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if not content or block_size > len(content):
                print('File is too short')
                return

            middle_index = len(content) // 2

            print(f"Beginning: {content[:block_size]}")
            print(f"Middle: {content[
                # i decided just to print second symbol from two
                middle_index-block_size//2: middle_index + block_size//2+1]}")
            print(f"End: {content[-block_size:]}")

    except FileNotFoundError:
        print(f"{file_path}' not exist")


if __name__ == '__main__':
    file_path = 'HT9/text.txt'
    block_size = 1
    extractor(file_path, block_size)
