""" Generates a list of [b, N, n] where N is the amount of b-bit primes
    and n is the amount of b-bit safe primes. """

import gmpy
import json

for b in xrange(1,33):
    N = 0
    n = 0
    p = gmpy.mpz(2**b)
    while True:
        p = gmpy.next_prime(p)
        if p > 2**(b+1):
            break
        if gmpy.is_prime(2*p + 1):
            n += 1
        N += 1
    d = n/float(N)
    print json.dumps([b, N, n])
            
