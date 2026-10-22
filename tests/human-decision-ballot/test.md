# Pressure test: human-decision-ballot

Type: output shape.
Cost: one agent, two short text files, under 3 minutes.

## Setup (once per arm)
Copy `fixture/` to a fresh folder; cwd = that folder.

The notes hold 5 real decisions (logo, load time, tutorial length, colorblind
colors, editor vs online), one settled question (max players) that must NOT be
asked, and one trivial item (credits font) that should be decided by the agent
or deferred, not put to the owner as equal weight.

## Prompt (verbatim)
> Here are your overnight notes (run_notes.md) and our decisions log
> (DECISIONS.md). Write the morning message to the project owner. They'll read it
> on their phone between meetings and want to unblock you for tonight.

## Failure signature (baseline)
Any one counts:
- Questions asked open-ended ("what would you like to do about the tutorial?")
  for 2 or more items.
- No recommendation on 2 or more decisions.
- Asks about max players again.
- Decisions scattered through narrative prose instead of a numbered list.
- No evidence path on the logo or colorblind items even though the notes name
  the images.

## Pass signature (with skill)
- One numbered list; lettered options; recommended option first with a one-line
  reason; a reply format offered ("1a 2b ...").
- Evidence paths attached (shots/logo_gold.png, shots/cb_sim.png, the 6.1s
  measurement marked measured and the 4.5s marked untested).
- Max players not asked (may be mentioned as still holding).
- Font decided by the agent or parked last as non-blocking.
- Editor-vs-online placed early (it blocks tonight's work).

## How to score
Checklist against the five failure items; pass needs all five avoided.
