'''
Created on 7 de mar de 2017

@author: wendell
'''

from .numbers import random_prime

def print_percent(percent):
    print(percent, "%\b\b\b\b\b\b\b\b", end=' ')
    sys.stdout.flush()


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


class RSA:

    def encode_str(self, m, pubk, verbose=False):
        n = pubk[0]
        e = pubk[1]
        c = []

        msg = [ord(ch) for ch in m]

        i = 0
        size = len(msg)
        perc = 0
        for ch in msg:
            c.append((ch ** e) % n)

        return c

    def decode_str(self, c, privk):
        n = privk[0]
        d = privk[1]
        m = []

        i = 0
        size = len(c)
        perc = 0
        for ch in c:
            i = i + 1
            m.append((ch ** d) % n)

        return ''.join(chr(i) for i in m)
