# Compare the level tables of the three machines: every key (r, W) known for one machine is recomputed for the others.
# usage: python3 compare_tables.py   (after run_levels.py / closure.py have stored tables in ../data)
import pickle,os
from machines import MACHINES
from levelmap import LevelMap
T={}
for name in MACHINES:
    p=os.path.join('..','data','table_%s.pkl'%name)
    if os.path.exists(p): T[name]=pickle.load(open(p,'rb'))
maps={name:LevelMap(MACHINES[name][1],MACHINES[name][2]) for name in MACHINES}
for a in T:
    for b in MACHINES:
        if a==b: continue
        keys=list(T[a]); same=0
        for k in keys:
            maps[b].TAB=T.get(b,{}) if b in T else maps[b].TAB
            same+= maps[b].entry(*k)==T[a][k]
        print('table of %s (%d entries) recomputed for %s: identical %d'%(a,len(keys),b,same))
