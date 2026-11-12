# Exact event rules of mirrored A (= M). Event X(m, S): state C, head on the blank cell left of the tape
# "0 0 1^m S", S = 0 1^a1 0 1^a2 ... written as the run list [a1, a2, ...]. One event = run to the next such moment.
# Tests the two main rules for all small m and k and several rests R.
# usage: python3 event_rules.py
import subprocess,re
from machines import MACHINES
M=MACHINES['A'][1]
def S2str(S): return ''.join('0'+'1'*k for k in S)
def event(m,S,maxsteps='4000000000'):
    r=subprocess.run(['./xmap',M,'00'+'1'*m+S2str(S),maxsteps],capture_output=True,text=True).stdout.split()
    if r[0]!='X': return r[0],None
    s=r[2]; mm=re.match(r'00(1+)',s)
    if not mm: return 'other form: '+s[:40],None
    rest=s[2+len(mm.group(1)):]
    if rest and not rest.startswith('0'): return 'other form: '+s[:60],None
    return len(mm.group(1)),([len(x) for x in rest[1:].split('0')] if rest else [])   # a run of length 0 is a '00'
if __name__=='__main__':
    RS=[[],[3],[3,6],[5,2,2,3],[8,2,2,2,3]]
    bad=0; n=0
    for m in range(2,120,3):
        for k in range(2,20):
            for R in RS:
                n+=1
                if event(m,[2,k]+R)!=(m+k+7,R): bad+=1; print('differs: main loop',m,k,R,event(m,[2,k]+R))
    print('main loop  m = 2 mod 3: X(m, [2,k]+R) -> X(m+k+7, R): %d cases (m <= 119, 2 <= k <= 19, %d rests), %d differ'%(n,len(RS),bad))
    bad=0; n=0
    for m in range(3,118,3):
        for k in range(2,20):
            for R in RS:
                n+=1
                if event(m,[k]+R)!=(4,[2]*(m//3)+[k+3]+R): bad+=1; print('differs: level end',m,k,R,event(m,[k]+R))
    print('level end  m = 0 mod 3: X(m, [k]+R) -> X(4, [2]^(m/3)+[k+3]+R): %d cases (m <= 117, 2 <= k <= 19, %d rests), %d differ'%(n,len(RS),bad))
