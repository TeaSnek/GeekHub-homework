"""
Створiть 3 рiзних функцiї (на ваш вибiр). Кожна з цих функцiй повинна
повертати якийсь результат (напр. інпут від юзера, результат математичної
операції тощо). Також створiть четверту ф-цiю, яка всередині викликає 3
попереднi, обробляє їх результат та також повертає результат своєї роботи.
Таким чином ми будемо викликати одну (четверту) функцiю, а вона в своєму тiлi
 - ще 3.
"""


def list_creator():
    return [x for x in range(12)]


def summer(nums: list):
    return sum(nums)


def egg(nums: list, sum_of_nums: int | float):
    return [x / sum_of_nums for x in nums]


def func4():
    nums = list_creator()
    sum_of_nums = summer(nums)
    return egg(nums, sum_of_nums)


if __name__ == '__main__':
    print(func4())
