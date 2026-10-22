---
name: honest-claims
description: Use when writing a status report, verdict, PR description, summary, or handoff that contains numbers, timings, timestamps, pass/fail results, or statements that something works, and when relaying another agent's or tool's results to a human
---

# Honest Claims

## Overview
A report is only useful if the reader can tell what was measured from what was
guessed. Every number and every "it works" carries how it is known.

Core principle: **say how you know, in the same sentence as what you know.**

## When to Use
- Any report with numbers, percentages, timings, counts, or clock times.
- Any statement that a fix works, a test passes, a build shipped.
- Passing on a subagent's or tool's result.
- Writing a decision record that cites evidence.

## The three claim tiers
Tag the claims that matter with one of these:

| Tier | Meaning | Example |
|---|---|---|
| PREDICTED, THEN MEASURED | You wrote the expected value down first, then measured | "Predicted -6620; measured -6624.7." |
| MEASURED | Measured, no prior prediction | "Gate passes 164/164 (log: verify_out/w3b/gate.log)." |
| INFERRED | Reasoning, no direct measurement | "Probably unreadable at a glance (inferred; not user-tested)." |

Predicted-then-measured is the strongest. Keep wrong predictions in the record
next to the measurement; they show the instrument is not echoing you.

## Rules
1. **Numbers are measured or marked.** A number names its source (a test, a
   log, a profiler, a count), or it is marked "arithmetic, not measured" with
   the working shown. Do not combine numbers from different runs and present
   the result as measured.
2. **Say what a number means separately from what it is.** "0 failures in 21.2M
   sampled pairs (measured). That users will never hit one is inferred."
3. **One sample is not the whole.** "12 of 20 positions are hidden; I checked
   one and it was visible." Not "the user can see it."
4. **Failures go first.** If anything is red, the first line says so. Do not
   bury a failure under successes or call it "mostly passing." A known failure
   that ships is listed as a known failure, with its numbers.
5. **Read the verdict, not the exit code.** Quote the PASS/FAIL line itself.
   Many scripts exit 0 on failure.
6. **Times come from the clock.** Run `date` (or the platform equivalent) before
   writing a timestamp or a duration. Never estimate a time and write it as if
   read.
7. **Pass results on with their source.** "The subagent reports X (not
   re-checked)" or "The subagent reports X; I re-ran it: same result."
8. **Committed is not agreed.** A file in git is not the accepted version until
   someone accepts it. Write "committed at <sha>" or "accepted by <who> at
   <sha>", and pin the agreed version by commit or hash.
9. **State the limits of the check.** What the test cannot see goes in the
   report: "checked on stills, not in motion"; "proven on the port, not yet in
   the shipped build."
10. **Correct in place, visibly.** When an earlier claim was wrong, add a dated
    correction next to it. Do not silently rewrite it.

## Self-check before sending
- Does every number have a source or a "not measured" mark?
- Is any failure, regression, or skipped check in the first lines?
- Did I separate what was measured from what it means?
- Did timestamps come from a clock?
- Did I say which results I re-checked myself?

## Common Mistakes
| Rationalization | Reality |
|---|---|
| "It's obviously right, no need to tag it" | Untagged claims get read as measured |
| "The script exited 0" | Many scripts exit 0 on FAIL |
| "Roughly 3 seconds" (never timed) | Mark it not measured, or time it |
| "The subagent confirmed it" | You passed it on; say whether you checked |
| Rewriting a wrong number in an old report | Readers can no longer trust any old number |
| "Upper bound" on something only sampled | Say what was sampled; a bound needs proof |
| "It's merged, so it's the agreed version" | Say who accepted it, at which sha |
