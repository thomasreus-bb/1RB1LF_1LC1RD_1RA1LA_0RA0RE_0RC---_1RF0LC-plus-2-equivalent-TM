# Compare the level maps of the three machines on all reachable tails (closure.py output, both residues):
# every entry (r, W) is computed (or taken from the stored table) for each machine and compared.
# usage: python3 compare_tables.py
import pickle,os
from machines import MACHINES
from levelmap import LevelMap
maps={}
for name in MACHINES:
    g=LevelMap(MACHINES[name][1],MACHINES[name][2])
    p=os.path.join('..','data','table_%s.pkl'%name)
    if os.path.exists(p): g.TAB=pickle.load(open(p,'rb'))
    maps[name]=g
keys=set()
for name in MACHINES:
    for W in pickle.load(open(os.path.join('..','data','reachable_%s.pkl'%name),'rb')):
        keys.add((0,W)); keys.add((1,W))
diff=0
for k in keys:
    vals=[maps[name].entry(*k) for name in MACHINES]
    diff+= not (vals[0]==vals[1]==vals[2])
print('%d entries (r, W) over the reachable tails of A, B and C; entries that differ between the machines: %d'%(len(keys),diff))
for name in MACHINES: pickle.dump(maps[name].TAB,open(os.path.join('..','data','table_%s.pkl'%name),'wb'))
