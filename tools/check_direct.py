# Check the level map against direct simulation: (1) the first levels of the real run, simulated directly from the
# blank tape; (2) random (n, W): table entry (shift-invariant in q) versus a direct one-level simulation.
# usage: python3 check_direct.py A|B|C
import sys,random,subprocess
from machines import MACHINES
from levelmap import LevelMap
name=sys.argv[1]; tm,table,state,(n0,W0)=MACHINES[name]
g=LevelMap(table,state)
n,W=n0,W0; seq=[(n,W)]
for i in range(12):
    n,W=g.direct(n,W); seq.append((n,W))
n,W=n0,W0; ok=True
for x in seq[1:]:
    n,W=g.level(n,W); ok&=((n,W)==x)
print('12 levels from (%d, %s): table iteration = direct simulation: %s'%(n0,W0,ok),' n =',[x[0] for x in seq])
rnd=random.Random(1); bad=0; T=40
for i in range(T):
    _,W=seq[rnd.randrange(1,len(seq))]; q=len(W)+40+rnd.randrange(0,300); r=rnd.randrange(2)
    e,W2=g.entry(r,W); n2,W3=g.direct(2*q+r,W)
    bad+= (W2 is None)!=(W3 is None) or (W2 is not None and (3*q+e,W2)!=(n2,W3))
print('%d random levels: table entry = direct simulation, differences: %d'%(T,bad))
