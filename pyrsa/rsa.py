'''
Created on 7 de mar de 2017

@author: wendell
'''

from multiprocessing import Pool
from functools import partial
from .numbers import random_prime

class KeyGenerator():
    '''
    classdocs
    '''

    def __init__(self, min=64, max=512):
        self.min = min
        self.max = max

    e = 0
    z = 0

    def generate(self, verbose=False):

        p = random_prime(self.min, self.max)
        q = random_prime(self.min, self.max)

        self._n = p * q
        self._z = (p - 1) * (q - 1)

        self._e = self._pick_e(self._n)
        self._d = self._pick_d(self._e, self._z)

        if (verbose):
            print("p: ", p)
            print("q: ", q)
            print("n: ", self._n)
            print("z: ", self._z)
            print("e: ", self._e)
            print("d: ", self._d)

    def _pick_e(self, n):
        return random_prime(n // 2, n - 1)

    def _pick_d(self, e, verbose=False):
        d = -1

        for d in range(2, self._z):
            if (e * d) % self._z == 1:
                if (verbose):
                    print("d found: ", d)
                    print("e * d: ", self._z * d)
                    print("(e * d) % z: ", (e * d) % self._z)
                return d

        if (verbose):
            print("d not found!")
        return d

    def get_public_key(self):
        return (self._n, self._e)

    def get_private_key(self):
        return (self._n, self._d)

def power(x, y, z):
    return pow(x, y, z)

class RSA:

    def __init__(self, key):
        self._key = key
        self._pubk = key.get_public_key()
        self._privk = key.get_private_key()

    # pow(ch, k, n) is faster than (ch**k % n)
    def encode_str(self, m, pool=True):
        n = self._pubk[0]
        e = self._pubk[1]
        c = []

        msg = [ord(ch) for ch in m]

        if pool:
            print ("Using 'map'")
            p = Pool()
            func = partial(power, y=e, z=n)
            c = p.map(func, msg)
        else:
            c = [pow(ch, e, n) for ch in msg]

        return c

    def decode_str(self, c, pool=True):
        n = self._privk[0]
        d = self._privk[1]
        m = []

        if pool:
            print("Using 'map'")
            p = Pool()
            func = partial(power, y=d, z=n)
            m = p.map(func, c)
        else:
            m = [pow(ch, d, n) for ch in c]

        return ''.join(chr(i) for i in m)

