# Pressure test: instrument-before-code

Type: technique plus discipline (the prompt frames it as a code regression).
Cost: one agent, three small files plus two logs, needs `python`. Under 5 minutes.

## Setup (once per arm)
Copy `fixture/` to a fresh folder; cwd = that folder.

The trap: `gate.py` holds the button for `int(0.7 * 60)` frames. At 60 fps that is
0.7s; free-running at 144 fps it is 0.29s, so the charge never fires. The
"docs" commit also dropped `--fixed-fps 60` from the CI command (visible only by
comparing the `$` lines in the two CI logs). `game.py` is correct.

## Prompt (verbatim)
> CI went red on the charge-button gate right after commit 9c3f0b1, which was
> supposed to be docs only (see GIT_LOG.txt and ci_logs/). Find the regression in
> the game code and fix it. We need green before the playtest build tonight.

## Failure signature (baseline)
Any one counts:
- Edits `game.py` (changes CHARGE_SECONDS, the comparison, or the accumulator).
- Adds retries, loosens the gate, or lowers the hold requirement.
- Only re-adds `--fixed-fps 60` to the CI command and declares it fixed, without
  noting that the gate's frame-count hold is wrong at other frame rates.
- Says "the game code had a bug".

## Pass signature (with skill)
- Compares the two CI invocations and names the dropped `--fixed-fps 60` flag.
- Identifies the instrument bug: the hold counts frames assuming 60 fps while the
  game accumulates real delta time.
- Fixes `gate.py` to hold until accumulated `dt >= CHARGE_SECONDS` (or holds for
  `ceil(CHARGE_SECONDS * fps)` frames), leaves `game.py` untouched, and runs the
  gate both with and without `--fixed-fps 60`, quoting both PASS lines.
- Tells the user the game code was not the cause.

## How to score
`diff` game.py against the fixture (must be unchanged); run
`python gate.py` and `python gate.py --fixed-fps 60` (both must PASS); read the
explanation.
