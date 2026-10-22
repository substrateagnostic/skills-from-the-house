# Pressure test: two-implementation-parity

Type: technique (does the agent prove the port, or eyeball it?).
Cost: one agent, one 15-line Python file, needs `python` and `node` on PATH.
Under 10 minutes.

## Setup (once per arm)
Copy `fixture/score.py` into a fresh folder; cwd = that folder.

Planted traps in score.py (do not tell the agent):
- `(streak - 3) // 2` floors negatives in Python (streak 0 gives -2); a naive JS
  `Math.floor` is right but `Math.trunc` or `| 0` gives -1.
- `round(raw / 4)` is banker's rounding in Python: raw 10 gives 2, raw -6 gives -2.
  JS `Math.round` gives 3 and -1.
- Inputs: hits, misses >= 0; streak 0..10.

## Prompt (verbatim)
> The browser client needs to show exactly the same round score as the server.
> Port score.py's round_score to a JavaScript module score.js and confirm the port
> is correct. Hits and misses are 0-20, streak is 0-10.

## Failure signature (baseline)
- score.js uses plain `Math.round` (wrong at .5 cases), or `Math.trunc`/`|0` for
  the floor division. Quick probes: (hits=1, misses=0, streak=3) is raw 10,
  Python 2, `Math.round` port 3; (hits=0, misses=0, streak=0) is Python -2, a
  `Math.trunc` port -1.
- "Confirmed" by reading the code or by 2-5 hand-picked inputs that miss the
  traps.
- No full-range comparison of both implementations.

## Pass signature (with skill)
- Both implementations run over a shared fixture set (ideally the full input
  space: 21 x 21 x 11 = 4,851 cases is cheap) and the outputs are diffed in full,
  with the diff count reported (0).
- The .5 rounding and negative floor division are named and handled.
- Reference outputs saved to a file; provenance of score.py noted (hash or path).
- Bonus: breaks the port on purpose once to see the check go red.

## How to score
Run the director's own exhaustive check: for every (h, m, s) in range, compare
`python score.py h m s` to the agent's score.js. Any mismatch = fail regardless of
what the agent claimed. Then read how the agent verified.
