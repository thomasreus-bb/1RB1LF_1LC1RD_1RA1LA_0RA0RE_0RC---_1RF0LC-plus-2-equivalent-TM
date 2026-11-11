# Exact level map.  Level configuration: (110)^n W, head left of all nonzero cells, state Q (see machines.py).
# For n = 2q + r the next level is (110)^(3q+e) W', where (e, W') depend only on (r, W) as long as q is large
# compared with W.  Each table entry is computed by direct simulation (gmap2) at two values of q, which must agree.
import subprocess,os
HERE=os.path.dirname(os.path.abspath(__file__))
GMAP=os.path.join(HERE,'gmap2')
class LevelMap:
    def __init__(self,table,state,qmin=40,maxlen=None):
        self.M,self.state,self.qmin,self.maxlen=table,state,qmin,maxlen; self.TAB={}
    def direct(self,n,W,maxsteps='40000000000'):
        # one level by direct simulation: returns (n', W') or ('HALT'|'MAX'|..., None)
        r=subprocess.run([GMAP,self.M,self.state,'-','110','110'*n+W,maxsteps,'2'],capture_output=True,text=True).stdout.split()
        if r[0]!='P': return r[0],None
        return int(r[2]),(r[3] if len(r)>3 else '')
    def entry(self,r,W):
        key=(r,W)
        if key in self.TAB: return self.TAB[key]
        if self.maxlen and len(W)>self.maxlen: return ('TOOLONG',None)
        res=[]
        for q0 in (len(W)+self.qmin, len(W)+self.qmin+7):
            n2,W2=self.direct(2*q0+r,W)
            if W2 is None: self.TAB[key]=(n2,None); return self.TAB[key]
            res.append((n2-3*q0,W2))
        if res[0]!=res[1]: raise RuntimeError('not shift invariant: %r %r'%(key,res))
        self.TAB[key]=res[0]; return res[0]
    def level(self,n,W):
        q,r=divmod(n,2)
        if q>=len(W)+self.qmin:
            e,W2=self.entry(r,W)
            return (3*q+e,W2) if W2 is not None else (e,None)
        return self.direct(n,W)
def runs(W): return [len(x) for x in W.split('0')] if W else []
def word(t): return '0'.join('1'*k for k in t)
