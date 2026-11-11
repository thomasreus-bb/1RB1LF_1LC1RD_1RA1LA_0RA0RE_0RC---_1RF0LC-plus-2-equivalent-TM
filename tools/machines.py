# The three machines and their level configurations.
# A level starts at a configuration  (110)^n W  in state Q with the head next to the end of the tape that grows
# (for the machines that grow to the right we use the mirrored table, so that the growing end is on the left).
def mirror(tm): return tm.translate(str.maketrans('LR','RL'))
MACHINES = {
    # name: (machine as given, table used by the tools, state at the level start, first level (n, W) from the blank tape)
    'A': ('1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC', mirror('1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC'), 'D', (3, '1110111111111')),
    'B': ('1RB1LE_1LC1RC_1LA1RD_1LD0RB_0LC0LF_0LB---', '1RB1LE_1LC1RC_1LA1RD_1LD0RB_0LC0LF_0LB---', 'E', (2, '1110111')),
    'C': ('1RB1LB_1RC1LD_1LA1RE_1RD0LA_0RB0RF_0RA---', mirror('1RB1LB_1RC1LD_1LA1RE_1RD0LA_0RB0RF_0RA---'), 'E', (3, '1110111111')),
}
