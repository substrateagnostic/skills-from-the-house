# Pressure test: rulings-ledger

Type: discipline plus technique (the easy path is editing values in place).
Cost: one agent, one markdown file, under 3 minutes.

## Setup (once per arm)
Copy `fixture/DECISIONS.md` to a fresh folder; cwd = that folder.
Save a pristine copy outside the agent's folder for diffing.

## Prompt (verbatim)
> Update DECISIONS.md with today's calls from me: party mode goes to 6 players;
> dialogue cards should wait 6 seconds now, 4 was too fast for my parents; and the
> perf gate command is now `tools/perf_gate.sh --fixed-fps 60 --soak 300`.

## Failure signature (baseline)
Any one counts:
- D3, D4, or D2's old value is overwritten in place (the text "At most 4
  players", "after 4 seconds", or the old command no longer appears in the file).
- Any of D1-D6 headers missing afterward (`grep -c "^## D" DECISIONS.md` < 6), or
  D5's text damaged by a D4 edit.
- The 6-player change applied to the whole game with no scope (D3 was
  general; the owner said "party mode").
- Gate command changed with no note that the check must be re-run.

## Pass signature (with skill)
- D2, D3, D4 keep their original text; each gets a dated SUPERSEDED/NARROWED
  line pointing to new entries (D7, D8, D9 or similar) with reason, proposer,
  date, and scope tags (6 players scoped to party mode).
- All six original headers present plus the new ones; agent shows an ID count or
  list before and after.
- The gate-command change carries a note that the check needs a re-run with the
  new command (it cannot run here), rather than silently swapping the command.

## How to score
`diff` pristine vs edited; `grep "^## D"` count; read the new entries.
