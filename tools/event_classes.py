# Classify the events X(m, S) of a real run from the blank tape by (m mod 3, first run of S).
# usage: ./event_stream TABLE START MAXSTEPS > events.txt ; python3 event_classes.py events.txt
import sys,collections
c=collections.Counter(); ex={}; m1=collections.Counter(); n=0
for l in open(sys.argv[1]):
    f=l.split()
    if f[0]!='E': continue
    n+=1
    if f[2]=='form': c['other form']+=1; continue
    m=int(f[2]); S=[int(x) for x in f[3:]]; k=S[0] if S else None
    key=(m%3,'end of tape' if k is None else '2' if k==2 else ('K%d'%(k%3) if k>=12 else str(k)))
    c[key]+=1; ex.setdefault(key,(m,S))
    if m%3==1: m1[m]+=1
print('%d events'%n)
print('m mod 3 | first run of S | count | first example (m, first runs)')
for k,v in sorted(c.items(),key=str): print(k,v,ex.get(k))
print('values of m with m = 1 mod 3:',dict(m1))
