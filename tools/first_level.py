# From the blank tape: the first configuration (110)^n W (n >= 2) in the level state, found by direct simulation.
# usage: python3 first_level.py A|B|C
import sys,subprocess,re
from machines import MACHINES
name=sys.argv[1]; tm,table,state,(n0,W0)=MACHINES[name]
out=subprocess.run(['./events',table,state,'100000000'],capture_output=True,text=True).stdout.split('\n')
for l in out:
    f=l.split()
    if len(f)==2:
        m=re.match(r'((?:110)+)(.*)$',f[1])
        if m and len(m.group(1))>=6:
            n=len(m.group(1))//3; W=m.group(2)
            print('machine %s: first level at step %s: n = %d, W = %s  (tools start from n = %d, W = %s): %s'%(name,f[0],n,W,n0,W0,(n,W)==(n0,W0)))
            break
