# Long (011)^j chains in the tail: start (110)^n HEAD (011)^j for small n and j up to F*n, follow up to L levels
# (direct simulation) until HALT or until the chain is used up.
# usage: python3 chains.py A|B|C NMIN NMAX F1,F2,... L HEAD1,HEAD2,...   (HEAD as dot-separated runs, e.g. 3.5)
import sys,collections
from machines import MACHINES
from levelmap import LevelMap,word
name=sys.argv[1]; tm,table,state,_=MACHINES[name]; g=LevelMap(table,state)
NS=range(int(sys.argv[2]),int(sys.argv[3])); FS=[float(x) for x in sys.argv[4].split(',')]; L=int(sys.argv[5])
heads=[[int(x) for x in h.split('.')] for h in sys.argv[6].split(',')]
c=collections.Counter()
for h in heads:
    for n0 in NS:
        for f in FS:
            j=max(1,int(f*n0)); n,W=n0,word(h)+'011'*j
            for lv in range(L):
                n2,W2=g.direct(n,W)
                if W2 is None: c[n2]+=1; break
                n,W=n2,W2
                if '011'*6 not in W: c['chain used up']+=1; break
            else: c['still running after L levels']+=1
print(dict(c))
