from datetime import datetime as dt
def timer(func):
    def tmp(*args, **kwargs):
        first_start = dt.now()
        print(f"Функция {func.__name__} стартовала в: {first_start}")
        res = func(*args, **kwargs)
        print(f"Время выполнения функции {func.__name__}: {dt.now() - first_start}")
        return res
    return tmp
