import gmpy
import json

for b in xrange(4,33):
    R = 0
    q = gmpy.mpz(2**(b-2))
    p = gmpy.mpz(2**(b-2))
    while True:
        p = gmpy.next_prime(p)
        if gmpy.is_prime(2*p+1):
            if p > 2 ** (b - 1):
                end = 2**(b-1)
            else:
                end = p
            R += int(end - q)
        if p > 2**(b-1):
            break
        q = p
    total = float(2**(b-2))
    print json.dumps([b, b*float(R)/total])
