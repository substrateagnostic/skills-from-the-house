# Project decisions

## D1. Engine is Godot 4.5
Decision: Build on Godot 4.5 stable.
Reason: team knows it; export to all targets.

## D2. Frame budget is 16.6ms
Decision: Every mode holds 60fps on the laptop.
Reason: measured baseline 11ms; 5ms headroom.
Check: run `tools/perf_gate.sh --fixed-fps 60`.

## D3. Max players is 4
Decision: At most 4 players.
Reason: four controllers on the couch during the first playtest.

## D4. Dialogue cards auto-advance after 4 seconds
Decision: Cards auto-advance after 4 seconds.
Reason: playtest said cards dragged.

## D5. Dialogue cards use 28px text
Decision: Cards use 28px text.
Reason: readable from the couch at 3m.

## D6. Saves go to slot 3 during tests
Decision: All test runs pass --slot=3.
Reason: slot 1 is the owner's real save.
