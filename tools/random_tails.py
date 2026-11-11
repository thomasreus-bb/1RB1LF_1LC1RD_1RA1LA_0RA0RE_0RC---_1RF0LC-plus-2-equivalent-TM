# Where can a HALT come from at all?  Random tails (random 0/1 words) after (110)^n, one level by direct simulation.
# usage: python3 random_tails.py A|B|C TRIALS NMAX LMAX P1
import sys,random,collections
from machines import MACHINES
from levelmap import LevelMap
name=sys.argv[1]; tm,table,state,_=MACHINES[name]; g=LevelMap(table,state)
T,NMAX,LMAX,p1=int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5])
rnd=random.Random(2); c=collections.Counter(); ex=[]
for t in range(T):
    n=rnd.randrange(2,NMAX); W='111'+''.join('1' if rnd.random()<p1 else '0' for _ in range(rnd.randrange(0,LMAX)))
    W=W.rstrip('0'); r,W2=g.direct(n,W,'3000000000')
    c['HALT' if r=='HALT' else 'level ends']+=1
    if r=='HALT' and len(ex)<8: ex.append((n,W))
print(dict(c))
for n,W in ex: print('HALT from n = %d, W = %s'%(n,W))
