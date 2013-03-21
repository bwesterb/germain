""" Graphs results collected by germaind.py """

import pyx
import math
import json

exact = []
with open('exact.jsons') as f:
    while True:
        l = f.readline()
        if not l:
            break
        d = json.loads(l[:-1])
        exact.append((d[0]+1, d[0]*(d[2]/float(d[1]))))

with open('germaind.jsons') as f:
    results = {}
    nlines = 0
    while True:
        nlines += 1
        if nlines % 50000 == 0:
            print nlines
        l = f.readline()
        if not l:
            break
        client, ts, bits, N, n  = json.loads(l[:-1])
        if not bits in results:
            results[bits] = [0, 0]
        results[bits][0] += N
        results[bits][1] += n
    data = []
    for b in sorted(results):
        N, n = results[b]
        p = float(n) / N
        z = 1.95996
        l = (p + z*z/(2*N) - z * math.sqrt((p*(1-p)+z*z/(4*N))/N))/(1+z*z/N)
        u = (p + z*z/(2*N) + z * math.sqrt((p*(1-p)+z*z/(4*N))/N))/(1+z*z/N)
        be = math.log(b, 2)
        print '%-10d %.4f %.4f %.4f %.4f %.8f %10d %10d' % (
                        b, l*b, p*b, u*b, (u-l)*b, p, N, n)
        data.append([b, l*(b-1), p*(b-1), u*(b-1)])

g = pyx.graph.graphxy(width=12,
        x=pyx.graph.axis.log(min=2, max=4096),
        y=pyx.graph.axis.linear(min=1.4, max=2.0))
g.plot(pyx.graph.data.points(exact, x=1, y=2),
            [pyx.graph.style.symbol(
                pyx.graph.style.symbol.plus, size=0.1)])
g.plot(pyx.graph.data.points(data, x=1, ymin=2, y=3, ymax=4),
            [pyx.graph.style.symbol(), pyx.graph.style.errorbar()])
c = 2 * 0.660161816 / math.log(2)
g.plot(pyx.graph.data.function("y(x) = c * (x-1) * (x - 2) / ((x-1)**2 + (x-1))",
                        context={'c': c}))
g.plot(pyx.graph.data.function("y(x) = c", context={'c': c}))
g.writePDFfile('graph.pdf')

# vim: se sw=4:et
