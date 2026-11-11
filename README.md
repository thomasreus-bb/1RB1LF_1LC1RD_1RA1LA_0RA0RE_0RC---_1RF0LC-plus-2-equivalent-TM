# Three BB(6) holdouts with one common Bell system

| name | machine | Holdout Guide | tape grows to the |
|---|---|---|---|
| A | `1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC` | #12, "Looks like a lottery: A 3/2 Bell. Every known halt needs a case that real transitions avoid." | right |
| B | `1RB1LE_1LC1RC_1LA1RD_1LD0RB_0LC0LF_0LB---` | #84, "Reported by others" | left |
| C | `1RB1LB_1RC1LD_1LA1RE_1RD0LA_0RB0RF_0RA---` | #440, "Looks like a lottery: A 3/2 Bell. Every known halt needs a case that real transitions avoid." | right |

Thomas Reus with Claude (Anthropic), 11 Nov 2026

## Summary

- The three machines are 3/2 Bells with the **same level map**. Every table entry that more than one of them uses gives the same result. They run one Bell system from three different starts.
- Exact level runs of 50,000 levels each (n up to about 10⁸⁸⁰⁶) show no HALT.
- Over **every** sequence of residues up to depth 400 (not only the likely ones), no tail leads to a HALT. Long chains in the tail are always used up without a HALT.
- A HALT was found only from tails that contain `00` or isolated single 1s. The real runs never produce these tails.
- So the three machines very probably never halt. **This is not a proof.** A non-halting proof of the common Bell system would decide all three machines; what is still missing is described below.

## The level map

For B the tape is used as it is. For A and C the mirrored table is used (L and R swapped), so that in all three cases the tape grows to the left.

- **Level configuration:** `(110)^n W` in state Q (Q = D for A, Q = E for B and C), with the head on the blank cell left of the tape. W is a short tail `1^a 0 1^b 0 1^c …`, written as the list of runs `[a, b, c, …]`.
- **Level map:** for n = 2q + r the next level configuration is `(110)^(3q+e) W′`. e and W′ depend only on (r, W) as long as q is large compared with the length of W.
- **How the table is computed:** each table entry (r, W) → (e, W′) is computed by direct simulation of one level, at two different values of q. The two results must agree, and they always did.
- **Checks:**
  - From the blank tape, the first level configuration appears after 234 steps (A: n = 3, W = `[3, 9]`), 70 steps (B: n = 2, W = `[3, 3]`) and 187 steps (C: n = 3, W = `[3, 6]`).
  - The first 12 levels from there are identical whether computed with the table or by direct simulation.
  - In 40 random levels per machine, the table entry and a direct simulation with another q agree (`data/check_direct.txt`).

| machine | n at the first levels |
|---|---|
| A | 3, 3, 8, 19, 48, 79, 129, 198, 304, 468, 709, 1068, 1609, … |
| B | 2, 4, 14, 28, 51, 81, 126, 196, 306, 466, 706, 1066, 1606, … |
| C | 3, 3, 8, 19, 52, 85, 132, 205, 312, 475, 717, 1080, 1627, … |

## Results

**Long runs** (`tools/run_levels.py`, `data/run_levels.txt`). 50,000 levels per machine, up to n ≈ 10⁸⁸⁰⁶: no HALT. The residues of n are equally distributed. The tail stays short: its entries are at most a few dozen, and a long entry is rare.

**Same level map** (`tools/compare_tables.py`). Every table entry of one machine that is recomputed for another machine gives the same (e, W′). This holds for all 3,436 entries met by A and B over all residue sequences.

**All residue sequences** (`tools/closure.py`, `data/closure.txt`). Starting from the first level of each machine, the tails were followed over every sequence of residues up to depth 400, for all tails up to 3,000 cells: no HALT. About 1,850 different tails appear. Only the branches with long chains `(011)^j` go over the cap.

For comparison, two other Bell-type holdouts of the same kind behave differently:
- `1RB1LF_1LC0RD_---1LA_0LA0RE_1LA1RA_1LB0LD` has a 35-level residue sequence that leads to a HALT; its HALT chance is about 1.1·10⁻¹⁴ per level.
- `1RB0LE_1LC0RD_0RA1LD_0LC1RA_1LF1LA_---1LA` halts when its tail counter catches up with the main counter.

Nothing like this was found here.

**Long chains** (`tools/chains.py`). Small n (4 … 59) were started with the short tail beginnings followed by a chain `(011)^j`, with j from 0.3·n to 60·n, and simulated directly for up to 80 levels. In all 8,110 runs the chain was used up without a HALT.

**Where a HALT can come from at all** (`tools/random_tails.py`, `data/random_tails_A.txt`). With completely random tails after `(110)^n`, one level halts in about 1 of 1,000 cases. Every HALT found needs `00` or isolated single 1s in the tail, for example W = `1111001010101111000101111`. The real runs never produce such tails.

## Towards a proof

**Grammar of the reachable tails** (`tools/grammar.py`). All tails reachable over all residue sequences (depth 400) have the form X* Y:
- blocks X = `3.5.2^j` (P) or `8.2^j` (Q), j ≥ 1;
- end Y = `[3t]` or `[3, 3t]`.

With two or more blocks the end is only `3` or `3.6`, and the later chains are short while the first chain can be long.

**Parametric rules** (`tools/rules.py`, for large n). In the following, e is the change of n beyond 3q.

| tail | r = 0 | r = 1 |
|---|---|---|
| `[3t]` | e = 6 + t, W′ = `[3]` | e = 6, W′ = `[3, 3t+3]` |
| `[3, 3t]` | e = 7, W′ = `[3t+3]` | e = 6, W′ = `3.5.2^(t−1).3` |

A level is a left-to-right pass over the blocks, with the residue carried along:
- a P block with r = 0 becomes a Q block (`3.5` → `8`), and everything behind it stays unchanged;
- a P block with r = 1 grows its chain (by 1 for even j, by 3 for odd j), and the next block is processed with residue 1 resp. 0;
- a Q block is swallowed into n: e grows by about 3j/2, an even chain length flips the residue, and the pass continues with the next block.

**Finer events** (mirrored A, `0 0 1^m S` in state C, head left of the tape, S as a list of runs). These two rules are exact, tested for all m < 120 and many tails:
- m ≡ 2 (mod 3): (m, `[2, k] + R`) → (m + k + 7, R).
- m ≡ 0 (mod 3): (m, `[k] + R`) → (4, `[2]^(m/3) + [k+3] + R`).

**What is missing.** For a proof the family of tails has to be closed for **all** parameter values, not only for the reachable ones.
- The simple grammar above is not closed in that sense. With a long second chain, a level can produce for example `3.0.K.2^j` (a `00`), or a P block with chain length 0. These forms disappear again after a few levels, and they never lead to a HALT.
- `tools/shapes.py` lets the family grow automatically. Every form is filled in with random parameters, and all successor forms are added. This gave several hundred forms with nested blocks and some new separators (`K` = a value ≡ 2 mod 3, `3.K`, `3.0.K`, `9.5`, `3.6.5`, `11`, …). No HALT appeared, but the family is infinite and has no simple description yet.

A proof needs:
1. a regular description of a family of tails that contains all reachable tails and is closed under the level map for all parameter values;
2. the level rules for this family with parameters, proved for all chain lengths, for example by symbolic execution in busycoq.

Ideas for step 1 are very welcome. A closed regular language could perhaps also be found directly by a CTL or MITM-DFA search with larger parameters than usual.

## Reproduce

    cd tools
    gcc -O2 -o gmap2 gmap2.c && gcc -O2 -o events events.c
    python3 first_level.py A            # first level from the blank tape (also B, C)
    python3 check_direct.py A           # table iteration and random levels vs. direct simulation
    python3 run_levels.py A 50000       # long run with tail statistics
    python3 closure.py A 400 3000       # all residue sequences up to depth 400
    python3 compare_tables.py           # tables of A, B, C compared
    python3 grammar.py A                # grammar of the reachable tails
    python3 rules.py                    # parametric rules
    python3 chains.py A 4 30 1,4,15 60 3.5,8,3
    python3 random_tails.py A 1000 200 60 0.6
    python3 shapes.py 12 1              # grow a closed family of shapes

Python 3 and gcc. `data/table_*.pkl` hold the computed table entries; without them the tools recompute everything, which takes longer.

| file | content |
|---|---|
| `tools/machines.py` | the three machines, their level states and first levels |
| `tools/gmap2.c` | one level by direct simulation |
| `tools/levelmap.py` | exact level map with the table of (r, W) → (e, W′) |
| `tools/events.c`, `tools/first_level.py` | direct simulation from the blank tape |
| `tools/check_direct.py` | checks against direct simulation |
| `tools/run_levels.py`, `tools/closure.py`, `tools/compare_tables.py` | long runs, closure over all residues, table comparison |
| `tools/chains.py`, `tools/random_tails.py` | long chains; where a HALT can come from |
| `tools/grammar.py`, `tools/rules.py`, `tools/shapes.py` | grammar, parametric rules, growing a closed family |
| `data/` | outputs of the tools and the computed tables |
