"""
Created on 8 de mar de 2017

@author: wendell
"""

from math import sqrt
from random import randint


def isprime(n):
    if n == 2 or (n != 1 and n % 2 == 1):
        prime = True
    else:
        prime = False

    div = 3
    while div < sqrt(n) and prime:
        if n % div == 0:
            prime = False
        div += 2

    return prime


def random_prime(min, max):
    n = randint(min, max)
    while not isprime(n):
        n = randint(min, max)
    return n
