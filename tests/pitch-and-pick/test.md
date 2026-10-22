# Pressure test: pitch-and-pick

Type: technique (does the agent decide by a pre-written rubric with a fallback?).
Cost: one agent, one markdown file, under 3 minutes. Pitches are supplied so no
sub-agents are needed; this tests steps 1 and 3-7. (Step 2, independent
pitching, is not exercised by this scenario; see tests/MANIFEST.md.)

## Setup (once per arm)
Copy `fixture/PITCHES.md` to a fresh folder; cwd = that folder.

## Prompt (verbatim)
> We're starting a 48-hour game jam in an hour. Three pitches are in PITCHES.md.
> Pick one and tell us how to start. Be decisive, we don't want a essay.

(The typo "a essay" is deliberate; leave it.)

## Failure signature (baseline)
Two or more:
- Picks by narrative preference with no stated criteria, or states criteria
  only after announcing the pick.
- No tiebreak or no scores per pitch.
- Losing pitches dropped entirely (no features carried over or parked).
- No early checkpoint for the winner's riskiest assumption, or no fallback named.

## Pass signature (with skill)
- Rubric with weights appears BEFORE the pick in the response.
- Each pitch scored per criterion with a one-line reason; tiebreak named.
- Steals listed from the two losers (e.g. C's "lights cut out at random" beat
  folded into A or B).
- Kill gate on the winner's riskiest assumption at roughly hours 6-10 of 48
  (e.g. B's lighting shader working), with a named fallback (often the
  runner-up).
- Still short; decisiveness is compatible with the structure.

## How to score
Order check (rubric before pick) plus the three remaining elements.
