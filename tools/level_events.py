# Link between level configurations and events of M (mirrored A).
# Level L(n, W): state D, head on the blank cell left of (110)^n W.  Event X(m, S): state C, head left of 0 0 1^m S.
# Checks: (1) L(n, W) runs directly into X(4, [2]^(n-1) + W);  (2) iterating events from there reaches
# X(4, [2]^(n'-1) + W') with (n', W') = the level map of (n, W).
# usage: python3 level_events.py
import pickle,re
from machines import MACHINES
from levelmap import LevelMap,word,runs
from event_rules import event
tm,table,state,_=MACHINES['A']
def parse(t):
    d={}
    for i,g in enumerate(t.split('_')):
        for s in (0,1):
            x=g[3*s:3*s+3]; d[('ABCDEF'[i],s)]=None if x[0]=='-' else (int(x[0]),x[1],x[2])
    return d
M=parse(table)
def first_event(n,W):
    s='110'*n+word(W); tape={i+1:int(c) for i,c in enumerate(s)}; pos=0; q='D'
    for st in range(10**6):
        nz=[i for i,v in tape.items() if v]
        if st>0 and q=='C' and pos<min(nz):
            t=''.join(str(tape.get(i,0)) for i in range(pos+1,max(nz)+1)); mm=re.match(r'00(1+)',t)
            rest=t[2+len(mm.group(1)):]; return st,(len(mm.group(1)),[len(x) for x in rest.split('0')[1:]])
        tr=M[(q,tape.get(pos,0))]
        if tr is None: return st,'HALT'
        tape[pos],d,q=tr; pos+=-1 if d=='L' else 1
g=LevelMap(table,state); g.TAB=pickle.load(open('../data/table_A.pkl','rb'))
cases=[(n,W) for n in (2,3,4,5,10,11,40,41) for W in ([3],[3,6],[9],[3,5,2,2,3],[8,2,2,2,3],[3,5,2,2,2,2,3,6],[12],[3,12])]
ok1=ok2=0
for n,W in cases:
    st,x=first_event(n,W); ok1+= x==(4,[2]*(n-1)+W)
    n2,W2=g.level(n,word(W)); target=(4,[2]*(n2-1)+runs(W2)); m,S=4,[2]*(n-1)+W; c=0
    while c<5000 and (m,S)!=target: m,S=event(m,S); c+=1
    ok2+= (m,S)==target
    print('L(%d,%s): first event after %d steps %s; next level %d %s reached after %d events'%(n,W,st,'= X(4,[2]^(n-1)+W)' if x==(4,[2]*(n-1)+W) else str(x),n2,runs(W2),c))
print('%d cases: (1) holds in %d, (2) holds in %d'%(len(cases),ok1,ok2))
