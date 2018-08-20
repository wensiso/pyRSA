"""
Created on 8 de mar de 2017

@author: wendell
"""

from math import sqrt
from random import randint

def isprime(n):
    if n == 2:
        return True
    
    if (n <= 1) or (n%2==0):
        return False
    
    div = 3
    while(div <= sqrt(n)):
        if n % div == 0:
            return False
        div += 2
        
    return True


def random_prime(minimum, maximum):
    n = randint(minimum, maximum)
    while not isprime(n):
        n = randint(minimum, maximum)
    return n
