"""
Написати функцію <bank> , яка працює за наступною логікою: користувач робить 
вклад у розмірі <a> одиниць строком на <years> років під <percents> відсотків
(кожен рік сума вкладу збільшується на цей відсоток, ці гроші додаються до
суми вкладу і в наступному році на них також нараховуються відсотки). Параметр
<percents> є необов'язковим і має значення по замовчуванню <10> (10%). Функція
повинна принтануть суму, яка буде на рахунку, а також її повернути (але 
округлену до копійок).
"""


def bank(a, years, percents=10):
    if a <= 0 or years <= 0 or percents < 0:
        raise ValueError('Inappropriate parameter value')

    balance = a
    for year in range(years):
        balance += balance * (percents / 100)

    balance = round(balance, 2)
    print(f"Balance: {balance}")

    return balance


if __name__ == '__main__':
    bank(2, 1000, percents=0.1)
