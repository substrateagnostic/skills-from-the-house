---
name: outside-judge
description: Use when a specification, format document, or protocol must be implementable by someone else; when judging whether a UI, image, or behavior reads correctly to a newcomer; when writing tests or fixtures for an implementation; or when a result would otherwise be graded by the same agent or person who produced it
---

# Outside Judge

## Overview
The author of a thing is the worst judge of whether it works for someone who
was not there. Use judges who have seen none of the work, give them only what a
real user would have, and decide what counts as passing before any answer
exists.

Core principle: **the pass line is written before the answers, and the judge
never saw the work.**

## When to Use
- A spec, file format, or API doc that another implementer must follow.
- A screen, still, or flow that must read correctly without explanation.
- A design question that can be settled by counting instead of opinion.
- New test fixtures for an implementation you or a teammate wrote.
- Any "it's good" that only the builder has checked.

## Pattern 1: Blind reader (for documents)
1. Spawn a fresh agent. Give it ONLY the document and the reference data a real
   implementer would get (fixtures, expected outputs). No source code, no
   earlier readers' notes, no conversation history.
2. It writes an **ambiguity list before writing any code**: each place the text
   allows two readings, the quote, both readings, which it picked and why. The
   list is append-only.
3. It implements from the document and runs against the reference data.
4. Diff its implementation against the real system on cases the document's own
   examples do not cover.
5. Every ambiguity is a document bug, even where the reader guessed right. Fix
   the document, not the reader.
6. Repeat with a NEW reader who has not seen the earlier ones. Each reader finds
   the layer the last round's fixes exposed. Stop when a fresh reader produces
   no ambiguities that change behavior, or record the rest as known limits.

A missing reference output is a failure, never a pass.

If you cannot spawn agents, the reviewer must still work from the document
alone: close the implementation, write the ambiguity list from the text, and
only then compare. Say in the report that this was a same-agent reading.

## Pattern 2: Sealed exam (for pictures, UX, behavior)
1. Fix the questions: the same questions for every item ("Where is the player?
   What can they do next? Is X still true?").
2. Write the answer key and **seal it**: save it where judges cannot read it and
   record its hash (`sha256sum KEY.json`) in the protocol before any judge runs.
3. Write the protocol before any answer: what is counted, the pass line ("at
   least 4 of 6 judges read it correctly"), what counts as unchanged and as
   worse, and control items that must not get worse. Say which numbers were
   chosen rather than measured.
4. Judges get only the items and the questions, in a clean folder. Each writes
   its own answer file and sees no one else's.
5. Commit or hash the answers before opening the key.
6. Mark with a fixed brief (right / partly / cannot tell / wrong; "mark what
   the answer says, not what it might have meant").
7. Where a result turns on one sentence, read the judges' words, not just the
   marks. Markers tend to be lenient.
8. Re-exams use fresh judges and the same questions byte for byte, so the build
   is the only thing that changed.
9. The verdict states what the exam cannot show ("models judging stills, not
   players in motion").

## Pattern 3: Hand answers before the run (for tests and fixtures)
- Before running an implementation on new fixtures, write the expected result
  for each by hand, from the spec, not from the code.
- Run. Where the implementation and the hand answer disagree, find out which is
  wrong. Both can be.
- Keep wrong hand answers in the record next to the result. They show the check
  was not just echoing the implementation.

## Pattern 4: Decide by measurement
When a design argument hinges on "would a user notice" or "can this be
exploited", write the decision rule first ("if zero exploitable cases in a
million samples, loosen the rule"), then measure at scale and apply the rule.
Record which part stayed inferred.

## Common Mistakes
| Mistake | Fix |
|---|---|
| Giving the reader the source code "for context" | It then checks the code, not the document |
| Reusing a judge across rounds | Fresh judges each round |
| Setting the pass line after seeing results | Write it in the protocol first, with the key's hash |
| Counting marks when the words disagree | Read the words on close calls |
| "The reader got it right, so the doc is clear" | An ambiguity is a bug even when guessed right |
| Builder picks the questions after seeing failures | Questions are fixed before the build under test |
| Expected test values copied from the implementation's output | Write them by hand from the spec first |
