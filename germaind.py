""" germaind.py collects approximations computed by germain.py """

import json
import time
import math
import random
import os.path
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
    print cur
    assert False

class GermainDRH(SocketServer.StreamRequestHandler):
    def handle(self):
        print '%s: connected' % self.client_address[0]
        try:
            while True:
                self.wfile.write(self.server.get_next_bits())
                self.wfile.write("\n")
                self.wfile.flush()
                l = self.rfile.readline()
                if not l:
                    break
                try:
                    d = json.loads(l[:-1])
                except ValueError:
                    print '%s: failed to parse %s' % (
                                    self.client_address[0], repr(l))
                    break
                if (not isinstance(d, list) or len(d) != 4 or
                            not isinstance(d[0], basestring) or
                            not isinstance(d[1], int) or
                            not isinstance(d[2], int) or
                            not isinstance(d[3], int)):
                    print '%s: invalid input %s' % (
                                    self.client_address[0], repr(l))
                    break
                client, bits, N, n = d
                self.server.register(client, bits, N, n)
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
    def register(self, client, bits, N, n):
        if not bits in self.results:
            print 'Ignoring record for bits %s' % bits
            return
        with self.lock:
            self.results[bits][0] += N
            self.results[bits][1] += n
            self.f.write(json.dumps([client, time.time(), bits, N, n]))
            self.f.write("\n")
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
        if os.path.exists('germaind.jsons'):
            with open('germaind.jsons') as f:
                while True:
                    l = f.readline()
                    if not l:
                        break
                    d = json.loads(l[:-1])
                    clientid, ts, bits, N, n = d
                    if bits not in self.results:
                        self.results[bits] = [0,0]
                    self.results[bits][0] += N
                    self.results[bits][1] += n
        self.f = open('germaind.jsons', 'a')
    def main(self):
        self.load()
        self.server_bind()
        self.server_activate()
        self.serve_forever()

if __name__ == '__main__':
    GermainD().main()
