# Pressure test: plain-prose-check

Type: output shape (polish without performing).
Cost: one agent, one 4-paragraph draft, under 3 minutes.

## Setup (once per arm)
Copy ONLY `fixture/about_draft.md` to a fresh folder; cwd = that folder.
Keep `keys/KEY_FOR_DIRECTOR.md` (14-15 planted devices, plus the facts that must
survive) for scoring.

## Prompt (verbatim)
> Polish about_draft.md for the About page on my website. It should sound like me,
> just better. Write the result to about_final.md.

## Failure signature (baseline)
Any one counts:
- about_final.md keeps 5 or more of the planted devices (count against the key).
- Introduces new devices: new dash asides, a new "not X, but Y", a new colon
  reveal, new stock phrases ("navigate", "landscape", "deeply", "genuinely").
- No change list; edits are silent.
- Drops or changes a fact on the key's must-survive list.

## Pass signature (with skill)
- 2 or fewer planted devices remain, and each one kept is listed as flagged
  with a reason (e.g. a possible signature phrase).
- No new devices.
- A change list: original, revised, device name.
- All must-survive facts present; sentences mostly shorter or equal in length.

## How to score
Count planted devices remaining in about_final.md using the key; scan for new
ones with a quick grep (`—`, `: `, "not .* but", "isn't about", the stock-phrase
list in SKILL.md), then read the flagged hits by hand.
