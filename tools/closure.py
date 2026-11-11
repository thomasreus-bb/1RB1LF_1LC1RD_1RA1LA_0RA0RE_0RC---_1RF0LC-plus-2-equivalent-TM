# Closure of the tails over ALL residue sequences (breadth first), from the first level of a machine.
# usage: python3 closure.py A|B|C DEPTH MAXLEN       reports any HALT; tails longer than MAXLEN cells are not followed
import sys,pickle,os
from machines import MACHINES
from levelmap import LevelMap
name=sys.argv[1]; D=int(sys.argv[2]); L=int(sys.argv[3])
tm,table,state,(n0,W0)=MACHINES[name]
g=LevelMap(table,state,maxlen=L)
p=os.path.join('..','data','table_%s.pkl'%name)
if os.path.exists(p): g.TAB=pickle.load(open(p,'rb'))
front={W0}; seen={W0}; over=0
for d in range(D):
    new=set()
    for W in front:
        for r in (0,1):
            e,W2=g.entry(r,W)
            if W2 is None:
                if e=='HALT': print('HALT at depth',d+1,'from tail',W,'r',r); sys.exit()
                over+=1; continue
            if W2 not in seen: seen.add(W2); new.add(W2)
    front=new
    if (d+1)%50==0: print('depth',d+1,'tails',len(seen),'over the cap',over,flush=True)
print('machine %s: no HALT for any residue sequence up to depth %d; %d tails, %d branches over %d cells'%(name,D,len(seen),over,L))
pickle.dump(g.TAB,open(p,'wb')); pickle.dump(seen,open(os.path.join('..','data','reachable_%s.pkl'%name),'wb'))
