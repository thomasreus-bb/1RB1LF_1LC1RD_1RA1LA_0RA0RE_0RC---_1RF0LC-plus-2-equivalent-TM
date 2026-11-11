# Do the level orbits of A, B, C (= M started in states A, B, C) ever meet?
# usage: python3 orbits.py LEVELS
import sys,pickle,math
from machines import MACHINES
from levelmap import LevelMap
K=int(sys.argv[1])
def canon(n,W):
    while W.startswith('110'): n+=1; W=W[3:]
    return n,W
seq={}
for name in 'ABC':
    tm,table,state,(n,W)=MACHINES[name]
    g=LevelMap(table,state); g.TAB=pickle.load(open('../data/table_%s.pkl'%name,'rb'))
    s=[canon(n,W)]
    for i in range(K):
        n,W=g.level(n,W); s.append(canon(n,W))
    seq[name]=s
for a,b in [('A','B'),('A','C'),('B','C')]:
    S=set(seq[a]); c=sum(1 for x in seq[b] if x in S)
    print('%s and %s: level configurations in common (any level index, %d levels): %d'%(a,b,K,c))
print('level  n_A - n_B   n_A - n_C   (log10 |difference| for large levels)')
for i in list(range(0,30))+[50,100,200,500,1000,2000,K]:
    dAB=seq['A'][i][0]-seq['B'][i][0]; dAC=seq['A'][i][0]-seq['C'][i][0]
    f=lambda d: str(d) if abs(d)<10**8 else '~10^%.1f'%math.log10(abs(d))
    print('%5d  %10s  %10s'%(i,f(dAB),f(dAC)))
