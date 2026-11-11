# Grow a family of tail "shapes" that is closed under the level map for arbitrary parameters.
# shape: runs of the tail, chains of >= 2 twos as '2*', values >= 12 as 'K<value mod 3>', smaller values exact.
# Every shape is filled in REP times with random parameters; all successor shapes (both residues) are added.
# usage: python3 shapes.py REP SEED   (starts from the shapes of ../data/reachable_A.pkl)
import random,sys,pickle,os
from machines import MACHINES
from levelmap import LevelMap,runs,word
tm,table,state,_=MACHINES['A']; g=LevelMap(table,state,maxlen=4000)
p=os.path.join('..','data','table_A.pkl')
if os.path.exists(p): g.TAB=pickle.load(open(p,'rb'))
REP=int(sys.argv[1]); rnd=random.Random(int(sys.argv[2]))
def shape(t):
    out=[];i=0
    while i<len(t):
        if t[i]==2:
            j=i
            while j<len(t) and t[j]==2: j+=1
            out.append('2' if j-i==1 else '2*'); i=j; continue
        out.append(str(t[i]) if t[i]<12 else 'K%d'%(t[i]%3)); i+=1
    return tuple(out)
def fill(sh,JM,KM):
    t=[]
    for x in sh:
        if x=='2*': t+=[2]*rnd.randrange(2,JM)
        elif x.startswith('K'): t.append(3*rnd.randrange(4,KM//3)+int(x[1]))
        else: t.append(int(x))
    return t
S=set(shape(runs(W)) for W in pickle.load(open(os.path.join('..','data','reachable_A.pkl'),'rb')))
todo=list(S); halts=0; levels=0
while todo:
    sh=todo.pop()
    for k in range(REP):
        t=fill(sh,rnd.choice([4,8,20,50]),rnd.choice([40,120,300]))
        for r in (0,1):
            e,W2=g.entry(r,word(t)); levels+=1
            if W2 is None:
                halts+= e=='HALT'; continue
            s2=shape(runs(W2))
            if s2 not in S: S.add(s2); todo.append(s2)
print('levels %d, shapes %d, HALT %d'%(levels,len(S),halts))
pickle.dump(S,open(os.path.join('..','data','shapes.pkl'),'wb')); pickle.dump(g.TAB,open(p,'wb'))
