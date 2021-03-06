"""
Created on 7 de mar de 2017

@author: wendell
"""

from multiprocessing import Pool
from functools import partial
from .numbers import isprime, random_prime


class RSAKey:
    MIN_PQ = 16384
    MAX_PQ = 32768
        
    def __init__(self, p=0, q=0, verbose=False):
        if p!=0 and q!=0:
            self._build_keys(p, q, verbose)

    def _build_keys(self, p, q, verbose=False):
        if p > RSAKey.MIN_PQ and isprime(p):
            self._p = p
        else:
            self._p = random_prime(RSAKey.MIN_PQ, RSAKey.MAX_PQ)

        if q > RSAKey.MIN_PQ and isprime(q):
            self._q = q
        else:
            self._q = random_prime(RSAKey.MIN_PQ, RSAKey.MAX_PQ)

        self._n = self._p * self._q
        self._z = (self._p - 1) * (self._q - 1)

        self._e = random_prime(self._n // 2, self._n - 1)
        self._d = self._pick_d(verbose=True)

        if verbose:
            print("p: ", self._p)
            print("q: ", self._q)
            print("n: ", self._n)
            print("z: ", self._z)
            print("e: ", self._e)
            print("d: ", self._d)

    def _pick_d(self, verbose=False):
        d = -1
        for d in range(2, self._z):
            if (self._e * d) % self._z == 1:
                if verbose:
                    print("d found: ", d)
                    print("e * d: ", self._z * d)
                    print("(e * d) % z: ", (self._e * d) % self._z)
                return d
        print('d not found!')
        return d

    def auto_build(self, verbose=False):
        self._build_keys(RSAKey.MIN_PQ, RSAKey.MIN_PQ, verbose)

    def get_public(self):
        return self._n, self._e

    def get_private(self):
        return self._n, self._d

    def set_public(self, n, e):
        if e < n and isprime(e):
            self._n = n
            self._e = e
            self._d = 0
        return False

    def set_private(self, n, d):
        self._n = n
        self._e = 0
        self._d = d
        return True

def power(x, y, z):
    return pow(x, y, z)


class RSA:
    def __init__(self, key):
        self._key = key
        self._pubk = key.get_public()
        self._privk = key.get_private()

    # pow(ch, k, n) is faster than (ch**k % n)
    def encode_str(self, m, pool=True):
        n = self._pubk[0]
        e = self._pubk[1]

        msg = [ord(ch) for ch in m]

        if pool:
            p = Pool()
            func = partial(power, y=e, z=n)
            c = p.map(func, msg)
        else:
            c = [pow(ch, e, n) for ch in msg]

        return c

    def decode_str(self, c, pool=True):
        n = self._privk[0]
        d = self._privk[1]

        if pool:
            p = Pool()
            func = partial(power, y=d, z=n)
            m = p.map(func, c)
        else:
            m = [pow(ch, d, n) for ch in c]

        return ''.join(chr(i) for i in m)
