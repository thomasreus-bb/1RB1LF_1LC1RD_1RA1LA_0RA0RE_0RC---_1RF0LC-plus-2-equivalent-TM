# Notes for a non-halting proof

Working notes, as a starting point for a proof that the machine of this repo never halts. Read `README.md` first. Everything here can be checked with the tools in `tools/`, and the outputs are in `data/`.

Thomas Reus with Claude (Anthropic), 12 Nov 2026

## 1. Setup

**One machine.** M = mirrored A = `1LB1RF_1RC1LD_1LA1RA_0LA0LE_0LC---_1LF0RC`. The tape of M grows to the left.
- A (Holdout Guide #12) is M started in state A.
- B (#84) is M started in state B.
- C (#440) is M started in state C.

A proof that M never halts from any configuration of a family F decides all three, if F contains the first configuration of each start (`tools/machines.py`, `data/first_level.txt`) and F is closed under M.

**HALT.** The only undefined transition is E reading 1. M enters E only through D reading 1.

**Notation.** Tapes are read from the head to the right, away from the growing end. A run list [a₁, a₂, …] means `0 1^a₁ 0 1^a₂ …`. A run of length 0 is a `00`. A chain 2^j is `(011)^j`.

**Two kinds of configurations.**
- *Level* L(n, W): state D, head on the blank cell left of `(110)^n W`. W is a short tail, written as its run list. The level map L(n, W) → L(n′, W′) is described in `README.md`. It needs n large compared with W ("q large"), which a proof would rather avoid.
- *Event* X(m, S): state C, head on the blank cell left of `0 0 1^m S`, with S a run list. One event is the run to the next such moment (`tools/xmap.c`, `tools/event_rules.py`, function `event`).

**Events cover everything.** L(n, W) reaches X(4, [2]^(n−1) + W) after 8 steps. Iterating events from there reaches X(4, [2]^(n′−1) + W′), where (n′, W′) is the level map of (n, W). This was checked in 64 of 64 cases (`tools/level_events.py`, `data/level_events.txt`).

So the main counter n is simply the leading chain of S. A proof can work with events only: there is one uniform object (m, S), and no "q large" condition is needed.

## 2. Exact event rules

`tools/event_rules.py`, `data/event_rules.txt`.

- **Main loop.** For m ≡ 2 (mod 3): X(m, [2, k] + R) → X(m + k + 7, R).
  - Tested in 3,600 cases (m ≤ 119, 2 ≤ k ≤ 19, five rests R), all exact.
  - With k = 2 this eats a chain two units at a time and adds 9 to m.
- **Level end.** For m ≡ 0 (mod 3): X(m, [k] + R) → X(4, [2]^(m/3) + [k+3] + R).
  - Tested in 3,510 cases, all exact.
  - The 1^m becomes the new main chain. Since m ≈ 9n/2 after the chain is eaten, the new chain has length ≈ 3n/2: this is the 3/2 Bell.
- **Other cases: no general rule yet.** These are m ≡ 1 (mod 3), and m ≡ 2 (mod 3) with a first run k ≥ 3. They are periodic in k with period 3, but they depend on the following runs and can reach deep into S.

  Examples, all with R = [5, 2, 2, 3]:

  | m | first run k | result |
  |---|---|---|
  | 31 (≡ 1) | 3, 6, 9 | X(35, [2]^((k−3)/3) + [8, 2, 2, 3]) |
  | 31 (≡ 1) | 4, 7, 10 | X(36, [14, 3]), X(35, [3, 14, 3]), X(35, [2, 3, 14, 3]) |
  | 31 (≡ 1) | 5, 8, 11 | X(4, [2]^9 + [3, k+6, 5, 2, 3]) (level end) |
  | 32 (≡ 2) | 5, 8, 11 | X(38, [2]^((k−5)/3) + [8, 2, 2, 3]) |
  | 32 (≡ 2) | 6, 9 | X(39, [14, 3]), X(38, [3, 14, 3]) |
  | 32 (≡ 2) | 3, 4, 7, 10 | level end, e.g. X(4, [2]^10 + [3, 8, 5, 2, 3]) for k = 4 |

  Deriving these rules for all parameters, with the following runs as parameters too, is open work.

## 3. What the real run does

`tools/event_stream.c`, `tools/event_classes.py`, `data/event_classes_A.txt`. These are the 80,557 events in the first 3·10¹⁰ steps of A.

- 80,466 events (99.9 %) are the main loop: m ≡ 2 and S starts with 2.
- **Every event with m ≡ 1 (mod 3) has m = 4**, and its S starts with 2 or 3. These are level starts, or the event right after one.
- All other events are rare: m ≡ 0 with S starting with 5, 6 or 12; m ≡ 2 with S starting with 3, 6, 8, 9, 14 or 15.
- All runs are at least 2.

## 4. Reachable tails and the grown family

- **Reachable tails** (`README.md`, `data/closure.txt`, `data/grammar_A.txt`). Over all residue sequences up to depth 400 there are 3,443 tails, all of the form X* Y, with
  - blocks X = `3.5.2^j` (P) or `8.2^j` (Q);
  - end Y = `[3t]` or `[3, 3t]`.

  In these tails **no run is ≡ 1 (mod 3)**: about 1.2 million runs were counted, and all are ≡ 0 or ≡ 2.
- **Grown family** (`tools/shapes.py`, `data/shapes_A.txt`). 345 shapes, with up to 13 entries.
  - The values that occur are 2, 3, 5, 6, 8, 9, 11, K0 and K2 (K0, K2 = a value ≥ 12 that is ≡ 0 resp. ≡ 2 mod 3), plus 0.
  - Again no value is ≡ 1 (mod 3).
  - A `00` (run 0) occurs only as `3.0.K2`.
  - A later check found 16 further shapes, so the list is not closed. The shape notation is too fine; it is better to describe the family by a few rules.

## 5. A candidate invariant, and a problem with it

**Candidate family F (event level).** X(m, S) is in F when:
- m is any value;
- every run of S is ≡ 0 or ≡ 2 (mod 3), so there is no run 1, 4, 7, …;
- a run 0 (a `00`) appears only right after a run that is ≡ 0 (mod 3) and > 0 (this run may be m), and only before a run > 0.

This family was found from the data in section 4. The rule for `00` had to be widened twice: a `00` after m arises from the main loop (m ≡ 2 with k ≡ 0 gives m + k + 7 ≡ 0), and `3.0.K0` arises too.

**Tests.**
- *Events* (`tools/family_test.py`, `data/family_test.txt`): 80,000 random members of F, each taken one event forward. 79,999 successors are in F again, and 1 halts.
- *Levels*: 16,000 levels of the level-start version of F (tails without leading 2s, runs ≡ 0 or 2 mod 3, with `00` only between a run ≡ 0 and a run ≡ 2). No successor left the family and no HALT occurred.

**The problem: F contains halting configurations.** There is a parametric halting family:

  X(m, [8, 3, K, 2, 2, 21] + [2]^j) with m ≡ 1 (mod 3) and K ≡ 2 (mod 3) halts in one event exactly when **j ∈ {(2K+80)/3, …, (2K+80)/3 + 3}**.

  This was checked for K = 5 … 32 and m = 4 … 58.

This is an exact-hit condition: two counters (K and the chain length j) must match. Such a condition cannot be excluded by a simple regular rule on the run values alone.

**How the real run avoids this family** (from section 3): it only has m ≡ 1 when m = 4 and S starts with 2 or 3, never with 8. So F has to be narrowed at least to:
- m ≡ 1 (mod 3) only when m = 4 and S starts with 2 or 3;
- and every case that this condition introduces has to be closed again.

The rare event kinds in section 3 are the ones a closure proof has to handle by hand.

## 6. What a proof needs

1. **A closed family F′ ⊆ F** that contains the first event configurations of A, B and C, is closed under one event for **all** parameter values, and contains no halting configuration. Suggestions:
   - Work at the event level, abstract m by (m mod 3, whether m = 4), and abstract the runs by (value mod 3, small or large). Chains 2^j are abstract too, possibly with j mod 2.
   - Take the conditions from section 3 as the first guess, and grow F′ by sampled successors, as `tools/shapes.py` does, until it is closed.
   - Keep checking with direct simulation (`tools/event_rules.py`) that F′ contains no halting member. The halting family of section 5 shows that this can fail in unexpected places.
2. **The event rules of F′ with parameters**, proved for all chain lengths and run values. The busycoq style would be an abstract machine `f` on a `Config` built from lists of blocks, with each rule proved by symbolic execution. An example is `Eqv_Misc.v` in `ccz181078/busycoq`, module `TM10`: `to_config`, `f`, and the tactic `solve_v1` with `esx`. Rules with chains need small induction lemmas for passing over `(011)^j` and `1^m`.
3. **The start.** Rocq has to check that A, B and C, simulated from the blank tape, reach F′: 234, 70 and 187 steps to the first level configuration, plus 8 steps to the first event.

**Already tried, not to repeat:** the standard CTL deciders (CPS, RWL_mod, NG) in 43 parameter sets.

**Open questions**
- Exact rules for the event cases m ≡ 1, and m ≡ 2 with first run ≥ 3 (section 2).
- Does F narrowed by the conditions of section 3 become closed, or do new kinds of events appear?
- Can the halting family of section 5 be reached from any member of a candidate F′? If yes, that F′ is too large.
- Is there a simpler invariant on the level side, for example a counting argument showing that the exact hit of section 5 never happens?

## 7. Files for this note

| file | content |
|---|---|
| `tools/xmap.c`, `tools/event_rules.py` | one event by direct simulation; test of the two exact rules |
| `tools/level_events.py` | levels and events: L(n, W) = X(4, [2]^(n−1) + W) |
| `tools/event_stream.c`, `tools/event_classes.py` | events of the real run, classified |
| `tools/family_test.py` | test of the candidate family F, halting family scan |
| `data/event_rules.txt`, `data/level_events.txt`, `data/event_classes_A.txt`, `data/family_test.txt`, `data/shapes_A.txt` | outputs |

    cd tools
    gcc -O2 -o xmap xmap.c && gcc -O2 -o event_stream event_stream.c
    python3 event_rules.py
    python3 level_events.py
    ./event_stream 1LB1RF_1RC1LD_1LA1RA_0LA0LE_0LC---_1LF0RC A 30000000000 > events.txt && python3 event_classes.py events.txt
    python3 family_test.py 20000
