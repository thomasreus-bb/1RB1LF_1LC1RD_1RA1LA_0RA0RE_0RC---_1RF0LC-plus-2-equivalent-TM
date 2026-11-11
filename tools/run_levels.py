# Iterate the exact level map of one machine from its first level, with statistics of the tail.
# usage: python3 run_levels.py A|B|C LEVELS
import sys,math,collections,pickle,os
from machines import MACHINES
from levelmap import LevelMap,runs
name=sys.argv[1]; K=int(sys.argv[2])
tm,table,state,(n,W)=MACHINES[name]
g=LevelMap(table,state)
p=os.path.join('..','data','table_%s.pkl'%name)
if os.path.exists(p): g.TAB=pickle.load(open(p,'rb'))
H=collections.Counter(); R=collections.Counter(); mx=0
for i in range(K):
    n,W=g.level(n,W)
    if W is None: print('HALT/stop at level',i+1,n); break
    t=runs(W)[1:]; k=max(t) if t else 0; H[k]+=1; R[n%2]+=1; mx=max(mx,k)
print('machine %s (%s): %d levels, log10 n = %.1f, largest tail entry %d'%(name,tm,K,math.log10(n),mx))
print('residues of n:',dict(R))
tot=sum(H.values()); acc=0; out=[]
for k in sorted(H,reverse=True):
    acc+=H[k]; out.append('>=%d: %.2g'%(k,acc/tot))
print('tail entry k (fraction of levels):',', '.join(out))
pickle.dump(g.TAB,open(p,'wb'))
