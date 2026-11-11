# Check that the reachable tails (closure.py output) fit the grammar  X* Y,  X = 3.5.2^j | 8.2^j (j >= 1),
# Y = [3t] | [3, 3t];  print the statistics by number of blocks.
# usage: python3 grammar.py A|B|C
import sys,pickle,os,collections
from levelmap import runs
def parse(t):
    i=0; blocks=[]
    while True:
        if t[i:i+2]==[3,5] and i+2<len(t) and t[i+2]==2:
            j=i+2
            while j<len(t) and t[j]==2: j+=1
            blocks.append(('P',j-i-2)); i=j; continue
        if t[i:i+1]==[8] and i+1<len(t) and t[i+1]==2:
            j=i+1
            while j<len(t) and t[j]==2: j+=1
            blocks.append(('Q',j-i-1)); i=j; continue
        break
    rest=t[i:]
    if len(rest)==1 and rest[0]%3==0 and rest[0]>=3: return blocks,('Y',rest[0])
    if len(rest)==2 and rest[0]==3 and rest[1]%3==0 and rest[1]>=6: return blocks,('3.Y',rest[1])
    return None
if __name__=='__main__':
    S=pickle.load(open(os.path.join('..','data','reachable_%s.pkl'%sys.argv[1]),'rb'))
    stat=collections.defaultdict(list); bad=0
    for W in S:
        p=parse(runs(W))
        if p is None: bad+=1; continue
        stat[len(p[0])].append(p)
    print('%d tails, not in the grammar: %d'%(len(S),bad))
    for nb in sorted(stat):
        L=stat[nb]; ys=collections.Counter(y[0]+('=%d'%y[1] if y[1]<=12 else '>12') for _,y in L)
        line='blocks=%d: %d tails; ends %s'%(nb,len(L),dict(ys))
        for k in range(nb):
            v=[b[k][1] for b,_ in L]; line+='; chain %d: %d..%d'%(k+1,min(v),max(v))
        print(line)
