# Parametric level rules on structured tails (large n, both residues). W is given as a list of runs of ones.
# usage: python3 rules.py "print(show([3,9]))"   or run without arguments for the standard tables
import sys
from machines import MACHINES
from levelmap import LevelMap,runs,word
tm,table,state,_=MACHINES['A']; g=LevelMap(table,state)
def sh(t):
    s=[];i=0
    while i<len(t):
        j=i
        while j<len(t) and t[j]==t[i]: j+=1
        s.append('%d^%d'%(t[i],j-i) if j-i>2 else '.'.join([str(t[i])]*(j-i))); i=j
    return '.'.join(s) or 'e'
def show(t):
    out=[]
    for r in (0,1):
        e,W2=g.entry(r,word(t))
        out.append('r=%d: e=%+d  %s'%(r,e,sh(runs(W2))) if W2 is not None else 'r=%d: %s'%(r,e))
    return ' | '.join(out)
if len(sys.argv)>1: exec(sys.argv[1])
else:
    for t in range(1,6): print(('[%d]'%(3*t)).ljust(14), show([3*t]))
    for t in range(2,6): print(('[3,%d]'%(3*t)).ljust(14), show([3,3*t]))
    for j in range(1,6): print(('P%d+[3]'%j).ljust(14), show([3,5]+[2]*j+[3]))
    for j in range(1,6): print(('Q%d+[3]'%j).ljust(14), show([8]+[2]*j+[3]))
