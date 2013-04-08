""" Performs the first test suggested by Eric. """

import math
import time
import gzip
import msgpack

def main():
    last_update = 0
    cum = {}
    with gzip.open('germaind.msgpacks.gz') as f:
        unpacker = msgpack.Unpacker(f)
        while True:
            if time.time() - last_update > 5:
                last_update = time.time()
                print 'Read %.0fMB' % (f.tell() / 1024.0  / 1024.0)
                for b in sorted(cum):
                    n, m, sx, sy, sx2, sy2 = cum[b]
                    if not n or not m: continue
                    avgx2 = sx**2/float(n**2)
                    avgy2 = sy**2/float(m**2)
                    Sx2 = sx2/float(n) - avgx2
                    Sy2 = sy2/float(m) - avgy2
                    T = (sx/float(n) - sy/float(m)) \
                              / math.sqrt(Sx2/float(n) + Sy2/float(m))
                    print '%s bits' % (b-1),
                    print '  n=%s m=%s sx/n=%s sy/m=%s' % (n, m,
                                                sx/float(n), sy/float(m)),
                    print '  S_x^2=%s  S_y^2=%s' % (Sx2, Sy2),
                    print '  T=%s' % T
                print
            client, ts, bits, res = unpacker.unpack()
            if not bits in  cum:
                cum[bits] = [0,0,0,0,0,0]
            for rr in res:
                if rr[0]:
                    cum[bits][1] += 1
                    cum[bits][3] += rr[1]
                    cum[bits][5] += rr[1] ** 2
                else:
                    cum[bits][0] += 1
                    cum[bits][2] += rr[1]
                    cum[bits][4] += rr[1] ** 2


if __name__ == '__main__':
    main()

# vim: sw=4:et
