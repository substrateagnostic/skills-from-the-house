---
name: two-implementation-parity
description: Use when porting logic between languages or runtimes, when a deterministic core (simulation, solver, serializer, hash, scoring or game rules, financial calculation) is trusted by other parts of a system, or when you must show that a shipped component matches a model or reference version
---

# Two-Implementation Parity

## Overview
One implementation can only agree with itself. A second implementation, built
apart from the first, that must produce the same bytes on the same inputs
catches the bugs neither author would think to test. It also catches the
places where the "spec" was really just whatever the first code happened to do.

Core principle: **two implementations, built separately, must agree byte for
byte on shared fixtures, and a missing reference output is a failure.**

## When to Use
- Porting code (Python to JS, GDScript to C#, server to client).
- A core that many parts trust: rules engines, scoring, physics steps,
  serializers, checksums, money math.
- You need evidence that the shipped thing matches a reference model.

Not worth it for glue code, UI layout, or anything not deterministic. Make it
deterministic first (fixed seed, fixed timestep) or compare only the
deterministic part.

## Steps
1. **Write the behavior down as a document**, not just as code: exact output
   format, byte order, rounding mode, integer division and modulo rules for
   negatives, float formatting, ordering of collections, error cases. A port
   that has to guess the bytes only proves it guessed.
2. **Build fixtures from the document**, including the edges a language
   difference will hit: negative numbers in division and modulo, rounding at .5,
   large integers, empty inputs, unicode, NaN and infinity if they can occur.
   Write expected outputs by hand for a few (see outside-judge, Pattern 3).
3. **Build the second implementation from the document and fixtures**, not by
   translating the first line by line. Line-by-line translation copies the
   first one's bugs and misses the language's different defaults.
4. **Dump both outputs in one canonical text form** (fixed float formatting,
   sorted keys) and diff them in full, case by case. Never compare summaries
   or a handful of spot checks.
5. **Commit the reference outputs** next to the fixtures, so a machine that
   cannot run the first implementation can still check the second.
6. **Record provenance**: which source commit or file hash each implementation
   was built from. When the reference changes, the port is stale until re-diffed.
7. **Make the check a gate.** It fails on any diff and also fails if a
   reference file is missing. A missing file is never a pass.
8. **Every new behavior gets a fixture that tries to break the gate.** Before
   trusting a gate, change one implementation on purpose and watch it go red.

## Language traps worth a fixture
| Operation | Differs between |
|---|---|
| Integer division of negatives (`-7 // 2`) | Python floors (-4); JS `Math.trunc`, C, Rust, Go truncate (-3) |
| Modulo of negatives (`-7 % 3`) | Python 2; JS, C, Rust -1 |
| `round(2.5)` | Python banker's rounding (2); JS `Math.round` (3) |
| Float to string | Shortest repr vs fixed digits; `1e21` formatting |
| Map/dict iteration order | Insertion order vs hash order |
| String length | Bytes vs UTF-16 units vs code points |
| Integer overflow | Python unbounded; JS loses precision above 2^53 |

## Common Mistakes
| Mistake | Fix |
|---|---|
| "I ported it and tried three inputs" | Shared fixture set, full diff, edge cases included |
| Translating line by line | Build from the written behavior |
| Reference outputs only on one machine | Commit them |
| Gate passes when the reference file is absent | Missing reference = FAIL |
| Never seeing the gate fail | Break it on purpose once |
