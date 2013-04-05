""" germaind.py collects approximations computed by germain.py """

import time
import math
import random
import os.path
import msgpack
import threading
import SocketServer

def weightedChoice(choices):
    total_weight = sum([weight for choice, weight in choices])
    x = random.uniform(0, total_weight)
    cur = 0
    for choice, weight in choices:
        cur += weight
        if cur >= x:
            return choice
    assert False

class GermainDRH(SocketServer.StreamRequestHandler):
    def handle(self):
        print '%s: connected' % self.client_address[0]
        unpacker = msgpack.Unpacker()
        self.wfile.write(msgpack.dumps(self.server.get_next_bits()))
        self.wfile.flush()
        try:
            while True:
                try:
                    d = unpacker.unpack()
                except msgpack.OutOfData:
                    tmp = self.request.recv(4096)
                    if not tmp:
                        break
                    unpacker.feed(tmp)
                    continue
                if (not isinstance(d, list) or len(d) != 3 or
                            not isinstance(d[0], basestring) or
                            not isinstance(d[1], int) or
                            not isinstance(d[2], list)):
                    print '%s: invalid input %s' % (
                                    self.client_address[0], repr(d))
                    break
                client, bits, res = d
                self.server.register(client, bits, res)
                self.wfile.write(msgpack.dumps(self.server.get_next_bits()))
                self.wfile.flush()
        except IOError, e:
            print '%s: %s' % (self.client_address[0], e)
        print '%s: disconnected' % self.client_address[0]
class GermainD(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self):
        SocketServer.TCPServer.__init__(self, ('0.0.0.0', 19102), GermainDRH,
                                        False)
        self.allow_reuse_address = True
        self.results = {}
        self.lock = threading.Lock()
    def register(self, client, bits, res):
        if not bits in self.results:
            print 'Ignoring record for bits %s' % bits
            return
        with self.lock:
            N = 0
            n = 0
            for entry in res:
                N += 1
                if entry[0]:
                    n += 1
            print "%s: %sb %s %s" % (client, bits, N, n)
            self.results[bits][0] += N
            self.results[bits][1] += n
            self.f.write(msgpack.dumps([client, time.time(), bits, res]))
            self.f.flush()
    def bits_to_error(self):
        ret = {}
        with self.lock:
            for bits in self.results:
                N, n = self.results[bits]
                if N == 0 or n == 0:
                    ret[bits] = 37.0
                    continue
                p = float(n) / N
                z = 1.95996
                l = (p + z*z/(2*N)-z*math.sqrt((p*(1-p)+z*z/(4*N))/N))/(1+z*z/N)
                u = (p + z*z/(2*N)+z*math.sqrt((p*(1-p)+z*z/(4*N))/N))/(1+z*z/N)
                ret[bits] = (u - l)/p
        return ret
    def get_next_bits(self):
        return weightedChoice(self.bits_to_error().items())
    def load(self):
        """ Loads state from the log file. """
        if os.path.exists('germaind.msgpacks'):
            with open('germaind.msgpacks') as f:
                unpacker = msgpack.Unpacker(f)
                while True:
                    try:
                        d = unpacker.unpack()
                    except msgpack.OutOfData:
                        break
                    clientid, ts, bits, res = d
                    if bits not in self.results:
                        self.results[bits] = [0,0]
                    N = 0
                    n = 0
                    for entry in res:
                        N += 1
                        if entry[0]:
                            n += 1
                    self.results[bits][0] += N
                    self.results[bits][1] += n
        self.f = open('germaind.msgpacks', 'a')
    def main(self):
        self.load()
        self.server_bind()
        self.server_activate()
        self.serve_forever()

if __name__ == '__main__':
    GermainD().main()
