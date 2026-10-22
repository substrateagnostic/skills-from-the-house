---
name: prompt-deepener
description: Use when writing a brief or prompt for a subagent, another model, or a work session on creative, research, design, or open-ended engineering work; when a task looks like it could be done adequately in an hour; or when the person asked for ambitious or professional-grade results
---

# Prompt Deepener

## Overview
A short brief gets a short answer: the agent does the obvious version and stops.
Asking for "more" makes the work longer, not better. Asking for what an expert
in the field would actually do, starting from the material they would start
from, and checked by something other than the author, makes it better.

Core principle: **go deeper, not bigger. Ask for the expert's raw material,
methods, and outside check, in plain words.**

## When to Use
- Briefing a subagent or another model on non-routine work.
- The first draft of the brief is one or two sentences.
- The person asked for ambition, quality, or "do it properly".

Not for mechanical tasks (rename, reformat, bump a version).

## The four questions
Answer each in a line or two before rewriting the brief.
1. **What would a top professional in this field do here that the brief does not
   ask for?** Name the field. If several fields touch the problem, list them.
2. **What raw material would they start from?** Primary sources, raw data, logs,
   the shipped binary, the actual user, not summaries or memory.
3. **What specific methods and tools do they use?** Named techniques,
   instruments, or procedures ("a constraint solver", "a contrast-ratio check",
   "a blind reader round"), not adjectives like "rigorous".
4. **What, besides the author's opinion, would show the result is right?** A
   measurement, an outside judge, a second implementation, a test the result
   could fail.

## Rewriting the brief
- **Turn nouns into verbs to find the fields.** "A shadow puzzle" becomes
  "proving where shade falls", which points at geometry solvers and astronomy.
- **Ask for actions, not a persona.** "Measure the contrast ratio of every
  label" beats "You are a world-class accessibility expert."
- **Question the format.** Ask what the deliverable is for. Sometimes the right
  output is a prototype, a measurement, or a decision, not the document asked
  for.
- **State the goal high and plainly.** Say what excellent looks like and how it
  will be checked.
- **Name the outside check in the brief**, with its pass line, so the agent can
  aim at it.

## Add an early kill gate
Ambitious work needs a cheap early test of its riskiest assumption.
- Name the one thing that, if it fails, makes the plan worthless (the core
  visual reads, the solver finishes in time, the data exists).
- Set a checkpoint early in the budget (for example, the first fifth of the
  time) where that thing must be shown working.
- Write the fallback now: if the checkpoint fails, what the agent switches to.
  Decide it before the work starts, not at the checkpoint.

## Brief template
```
Goal: <what excellent looks like, one or two sentences>
Start from: <raw material, with paths or sources>
Methods: <named techniques or tools the field uses>
Check: <outside measure or judge, and the pass line>
Kill gate: by <time or step>, show <core assumption working>; else <fallback>
Deliver: <format, and why that format>
```

## Common Mistakes
| Mistake | Fix |
|---|---|
| "Be thorough and creative" | Name the methods and the check |
| "You are an expert X" | Ask for the actions an expert takes |
| Making the task bigger (more pages, more items) | Make it deeper (better sources, a real check) |
| No early test of the risky part | Kill gate with a pre-written fallback |
| Accepting the requested format unexamined | Ask what the output is for |
