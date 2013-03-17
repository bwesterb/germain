""" Graphs results collected by germaind.py """

import pyx
import math
import json

with open('germaind.jsons') as f:
    results = {}
    while True:
        l = f.readline()
        if not l:
            break
        client, ts, bits, N, n  = json.loads(l[:-1])
        if not bits in results:
            results[bits] = [0, 0]
        results[bits][0] += N
        results[bits][1] += n
    data = []
    for b in results:
        N, n = results[b]
        p = float(n) / N
        z = 1.95996
        l = (p + z*z/(2*N) - z * math.sqrt((p*(1-p)+z*z/(4*N))/N))/(1+z*z/N)
        u = (p + z*z/(2*N) + z * math.sqrt((p*(1-p)+z*z/(4*N))/N))/(1+z*z/N)
        be = math.log(b, 2)
        print '%-10d %.4f %.4f %.4f %.4f %.8f' % (b, l*b, p*b, u*b, (u-l)*b, p)
        data.append([b, l*b, p*b, u*b])

g = pyx.graph.graphxy(width=12,
        x=pyx.graph.axis.log(min=16, max=4096))
g.plot(pyx.graph.data.points(data, x=1, ymin=2, y=3, ymax=4),
            [pyx.graph.style.symbol(), pyx.graph.style.errorbar()])
g.writePDFfile('graph.pdf')
