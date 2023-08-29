import csv
import json
import math
import random
from random import randint
from typing import Callable


def find_square_roots(a: int, b: int, c: int) -> tuple:
    discriminant = b ** 2 - 4 * a * c
    if discriminant > 0:
        return (-b + math.sqrt(discriminant)) / (2 * a), \
               (-b - math.sqrt(discriminant)) / (2 * a)
    if discriminant == 0:
        return -b / (2 * a), None
    return None, None


def generate_sq_rt_coef_in_csv():
    with open("sq_rt_coef.csv", "w", newline="") as file:
        for _ in range(randint(100, 1001)):
            csv.writer(file).writerow([randint(1, 10) * random.choice([-1, 1]),
                                       randint(1, 10) * random.choice([-1, 1]),
                                       randint(1, 10) * random.choice([-1, 1])])


def calculate_square_roots_from_csv(func: Callable):
    square_roots_list = []

    def wrapper(*args):
        coef = func(*args)
        for i in coef:
            square_roots_list.append(find_square_roots(*i))
        return square_roots_list

    return wrapper


def save_sq_rt_to_json(func: Callable):
    def wrapper(*args):
        sq_rt_list = func(*args)
        with open("sq_rt.json", "w") as file:
            lines = [json.dumps(i) for i in sq_rt_list]
            file.write(("\n".join(lines)))

    return wrapper


@save_sq_rt_to_json
@calculate_square_roots_from_csv
def get_coef_from_csv(filename: str) -> tuple:
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            yield tuple(map(int, row))


if __name__ == '__main__':
    generate_sq_rt_coef_in_csv()
    get_coef_from_csv("sq_rt_coef.csv")
