# Pressure test: outside-judge

Type: technique (does the agent judge the document from outside, or from the code
it can see?).
Cost: one agent (it may spawn one sub-reader if it has the tool), two small files,
under 10 minutes.

## Setup (once per arm)
Copy ONLY `fixture/` (SPEC.md and tally.py) into a fresh folder. Do NOT copy
`keys/NOTES_FOR_DIRECTOR.md`; it is the answer key (six planted ambiguities).

## Prompt (verbatim; cwd = that folder)
> I wrote SPEC.md and the reference implementation tally.py. Next week another
> team implements a TALLY reader in Rust from the spec alone; they won't see my
> Python. Check whether the spec is ready to hand off and tell me what, if
> anything, to fix.

## Failure signature (baseline)
- Reads tally.py and checks the spec against it ("the spec matches the
  implementation"), then calls the spec ready or nearly ready.
- Finds 2 or fewer of the 6 planted ambiguities (byte order; name length in bytes
  vs characters; checksum truncation; checksum byte order; name length limit;
  example without hex bytes).
- Proposes no outside check (no blind reader, no hex test vector, no
  "implement-from-spec-and-diff" step).

## Pass signature (with skill)
- Works from the spec alone before consulting the code (or hands the spec plus
  a test vector to a fresh sub-agent with no code), and says which it did.
- Produces an ambiguity list with quotes from the spec; finds 4 or more of the 6.
- Treats each ambiguity as a spec bug even where the "obvious" reading matches
  the code.
- Recommends adding concrete reference data (the hex for the example, edge-case
  vectors) and a blind-reader round after the fix.

## How to score
Count planted ambiguities found against keys/NOTES_FOR_DIRECTOR.md. Note whether the
code was read before or after the ambiguity list was written (check tool order).
