"""
Програма-світлофор.

Створити програму-емулятор світлофора для авто і пішоходів. Після запуска
програми на екран виводиться в лівій половині - колір автомобільного, а в
правій - пішохідного світлофора. Кожну 1 секунду виводиться поточні кольори.
Через декілька ітерацій - відбувається зміна кольорів - логіка така сама як
і в звичайних світлофорах (пішоходам зелений тільки коли автомобілям
червоний).

Приблизний результат роботи наступний:
    Red        Green
    Red        Green
    Red        Green
    Red        Green
    Yellow     Red
    Yellow     Red
    Green      Red
    Green      Red
    Green      Red
    Green      Red
    Yellow     Red
    Yellow     Red
    Red        Green
"""

from time import sleep


def switch(lights_dict, i=0):
    while True:
        yield lights_dict[i % len(lights_dict)]
        i += 1


def crossroad(iter=30):
    colors = {0: 'Green', 1: 'Yellow', 2: 'Red', 3: 'Yellow'}
    traffic_lights = switch(colors)
    current_auto = next(traffic_lights)
    curr_timeout, next_timeout = 6, 2
    for i in range(iter):
        print(f'{current_auto}|{'Green' if current_auto == 'Red' else 'Red'}')
        if i % curr_timeout == 0:
            current_auto = next(traffic_lights)
            curr_timeout, next_timeout = next_timeout, curr_timeout
        sleep(1)


if __name__ == '__main__':
    crossroad()
