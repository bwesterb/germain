""" germain.py approximates the number of safe primes """

import os
import sys
import time
import json
import socket
import base64

import gmpy
import Crypto
import Crypto.Random
import Crypto.Util.number as number

def count_safe_primes(bits):
    randfunc = Crypto.Random.new().read
    started = time.time()
    N = 0
    n = 0
    while True:
        N += 1
        q = gmpy.mpz(number.getRandomNBitInteger(bits-1, randfunc))
        q = gmpy.next_prime(q)
        p = 2*q + 1
        if gmpy.is_prime(p):
            n += 1
        if time.time() - started > 60:
            break
    return N, n

def main():
    s = socket.socket()
    s.connect(('sw.w-nz.com', 19102))
    f = s.makefile()
    if len(sys.argv) >= 2:
        client = sys.argv[1]
    else:
        client = base64.b64encode(os.urandom(5))
    while True:
        l = f.readline()
        if not l:
            break
        bits = int(l[:-1])
        N, n = count_safe_primes(bits)
        print bits, N, n
        f.write(json.dumps([client, bits, N, n]))
        f.write("\n")
        f.flush()

if __name__ == '__main__':
    main()
