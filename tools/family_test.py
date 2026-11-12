# Test a candidate invariant family F of event configurations X(m, S) (see NOTES_for_proof.md, section 5):
#   every run of S is = 0 or 2 (mod 3), so no run 1, 4, 7, ...; a run of length 0 (a '00') is allowed only
#   right after a run (or m) that is = 0 (mod 3) and > 0, and before a run > 0.  m itself is free.
# Random members of F are taken one event forward; the successor is checked for membership in F.
# Then the halting family found inside F is scanned.
# usage: python3 family_test.py N
import sys,random,collections
from event_rules import event
def inF(m,S):
    t=[m]+S
    for i in range(1,len(t)):
        k=t[i]
        if k==0:
            if not(t[i-1]>0 and t[i-1]%3==0 and i+1<len(t) and t[i+1]>0): return False
        elif k%3==1: return False
    return True
def sample(rnd,P00):
    m=rnd.randrange(2,300); t=[]
    for _ in range(rnd.randrange(1,12)):
        x=rnd.random(); prev=t[-1] if t else m
        if x<0.35: t+=[2]*rnd.randrange(1,rnd.choice([3,10,60]))
        elif x<0.35+P00 and prev%3==0 and prev>0: t+=[0,3*rnd.randrange(1,rnd.choice([5,40]))+rnd.choice([0,2])]
        else: t.append(3*rnd.randrange(1,rnd.choice([4,12,60]))+rnd.choice([0,2]))
    return m,t
N=int(sys.argv[1])
for seed,P00 in [(31,0.1),(32,0.1),(33,0.3),(34,0.3)]:
    rnd=random.Random(seed); out=collections.Counter(); ex=[]
    for i in range(N):
        m,S=sample(rnd,P00)
        if not inF(m,S): continue
        r=event(m,S,'200000000')
        if r[1] is None: out[r[0]]+=1; ex.append((m,S)); continue
        out['successor in F' if inF(*r) else 'successor not in F']+=1
    print('seed %d, P(00) = %.1f: %s'%(seed,P00,dict(out)))
    for x in ex[:3]: print('   example:',x)
H=lambda m,S: event(m,S,'100000000')[0]=='HALT'
print('halting family X(m, [8, 3, K, 2, 2, 21] + [2]^j), m = 4:')
for K in (5,8,11,14,17,20,23,26,29,32):
    print('   K = %d: HALT for j in %s'%(K,[j for j in range(0,4*K+30) if H(4,[8,3,K,2,2,21]+[2]*j)]))
print('   m with HALT for K = 20, j = 40:',[x for x in range(2,60) if H(x,[8,3,20,2,2,21]+[2]*40)])
