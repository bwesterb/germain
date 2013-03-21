germain
=======

These are a few small Python scripts to estimate the relative density
of the safe primes in the normal primes.  `p` is called a safe prime
if `(p - 1)/2` and `p` itself are prime.
Conversely, if both `p` and `2p+1` are prime, then `p` is called
a Sophie Germain prime.
For quite a few of cryptographic algorithms it is advised to
use safe primes.
Finding a b-bit safe prime is simple: simply generate a b-bit random prime and
then check whether it is safe.  It is simple, but it takes some time.
To estimate how long, we are interested in the relative density:
the fraction of b-bit primes that are safe.

To help out, clone this repository and run:

    apt-get install python-crypto python-gmpy
    python germain.py my-name
