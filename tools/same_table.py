# B and C are the mirrored table of A with the states renamed: all three are one machine M,
# started from the blank tape in different states.
import itertools
from machines import MACHINES
def parse(t):
    d={}
    for i,g in enumerate(t.split('_')):
        for s in (0,1):
            x=g[3*s:3*s+3]
            d[('ABCDEF'[i],s)]=None if x[0]=='-' else (int(x[0]),x[1],x[2])
    return d
def ren(tm,p): return {(p[q],s):(None if v is None else (v[0],v[1],p[v[2]])) for (q,s),v in tm.items()}
M=parse(MACHINES['A'][1])
print('M = mirrored A =',MACHINES['A'][1])
for nm in 'BC':
    X=parse(MACHINES[nm][1])
    for perm in itertools.permutations('ABCDEF'):
        p=dict(zip('ABCDEF',perm))
        if ren(M,p)==X:
            inv={v:k for k,v in p.items()}
            print('%s (table used by the tools) = M with states renamed %s; so %s is M started in state %s'%(
                nm,' '.join('%s->%s'%kv for kv in p.items()),nm,inv['A']))
