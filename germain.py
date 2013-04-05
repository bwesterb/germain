""" germain.py approximates the number of safe primes """

import os
import sys
import time
import socket
import base64
import msgpack
import multiprocessing

import gmpy
import Crypto
import Crypto.Random
import Crypto.Util.number as number

def count_safe_primes(bits):
    randfunc = Crypto.Random.new().read
    started = time.time()
    ret = []
    while True:
        r = gmpy.mpz(number.getRandomNBitInteger(bits-1, randfunc))
        q = gmpy.next_prime(r)
        p = 2*q + 1
        germain = gmpy.is_prime(p)
        ret.append((germain, int(q - r)))
        if time.time() - started > 60:
            break
    return ret

def main():
    sleep_time = 0.1
    while True:
        try:
            s = socket.socket()
            s.connect(('sw.w-nz.com', 19102))
            wfile = s.makefile('w') 
            unpacker = msgpack.Unpacker()
            sleep_time = 0.1
            if len(sys.argv) >= 2:
                client = sys.argv[1]
            else:
                client = base64.b64encode(os.urandom(5))
            while True:
                try:
                        bits = unpacker.unpack()
                except msgpack.OutOfData:
                        tmp = s.recv(4096)
                        if not tmp:
                                break
                        unpacker.feed(tmp)
                        continue
                res = count_safe_primes(bits)
                print bits, len(res)
                wfile.write(msgpack.dumps([client, bits, res]))
                wfile.flush()
        except socket.error as e:
            print "%s. sleeping %s" % (e, sleep_time)
            time.sleep(sleep_time)
            sleep_time = min(sleep_time * 2, 60)

if __name__ == '__main__':
    for i in xrange(multiprocessing.cpu_count()):
        print 'starting process #%s' % (i+1)
        multiprocessing.Process(target=main).start()
