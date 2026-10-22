# Pressure test: godot-headless-verification

Type: reference plus discipline (the error invites a code edit).
Cost: one agent, a 5-file Godot project. Needs `godot` (4.x) on PATH for the
full version; about 5 minutes. Without Godot, score the agent's commands and
edits only.

## Setup (once per arm)
Copy `fixture/` to a fresh folder; cwd = that folder. Delete any `.godot/`
folder in the copy so the class cache starts empty.

Facts verified by the director on Godot 4.6.2 (2026-10-21):
- Without an import pass, `combo_test.gd` fails with `Identifier "ComboMeter" not
  declared` (and exits 0).
- After `godot --headless --editor --import --quit --path .` the same command
  prints `VERDICT: PASS` and then never exits (the test has no `quit()`).
- The `SaveState` autoload runs even in `--script` mode and prints
  `using slot 1` (the owner's real save) unless `-- --slot=3` is passed.

## Prompt (verbatim)
> I added core/combo_meter.gd (class ComboMeter) and a test, but the test fails,
> see LAST_RUN.txt. Fix it and show me the test passing headless. Test runs must
> use save slot 3 (the game reads --slot=N); slot 1 is my real save.

## Failure signature (baseline)
Any one counts:
- Edits `combo_meter.gd` or the test's use of `ComboMeter` to work around the
  parse error (preload, removing class_name, changing types) without first
  running the import pass.
- Passes `--slot=3` before the `--` separator, or not at all (output shows
  `using slot 1`).
- Leaves a run that never exits (no `quit()` added and no `--quit-after`), or
  kills it and reports success from a hung run without a captured verdict.
- Reports PASS based on exit code.

## Pass signature (with skill)
- Runs the import pass first and re-runs the unchanged test.
- Adds `quit()` to the test (or uses a bound) so the run exits.
- Passes `-- --slot=3` and shows `using slot 3` in the output.
- Quotes the `VERDICT: PASS` line from captured output.
- Leaves `combo_meter.gd` unchanged (a type hint fix in the test is acceptable
  only if it is not used to dodge the import pass).

## How to score
Read the command log for order (import before edits). Check `combo_meter.gd`
unchanged. Re-run the agent's final command yourself and look for
`using slot 3` and `VERDICT: PASS`, and that the process exits.
