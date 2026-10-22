---
name: instrument-before-code
description: Use when a test, gate, benchmark, or measurement fails on code that should not have changed its result, when results look flaky or differ between runs or machines, when a metric does not move even though its subject changed, or when a performance number regresses without a code reason
---

# Instrument Before Code

## Overview
A failing measurement has three suspects: the code, the instrument (the test,
probe, or script), and the conditions (arguments, machine state, other running
work). Agents jump to the code. Often the code is innocent, and "fixing" it
hides the real problem or breaks something that worked.

Core principle: **when a measurement surprises you, check the instrument, the
invocation, and the machine before you touch the code.**

REQUIRED BACKGROUND: superpowers:systematic-debugging covers debugging the code
itself. This skill covers the step before it.

## When to Use
- A gate fails after a change that should not affect it (docs, config, an
  unrelated file).
- "Flaky": the same tree gives different verdicts.
- A metric holds steady while the thing it measures clearly changed.
- A timing or performance number moved and no code explains it.

## Checks, in order
1. **Diff the invocations.** Compare the exact command lines, flags,
   environment, and working directory of the passing and failing runs. If the
   tree is identical and the verdict differs, the arguments or the conditions
   decided it.
2. **Find the last passing run** and compare against that, not the nearest log
   by date.
3. **Check units and clocks in the instrument.** Frame counts are not seconds
   unless the frame rate is fixed. A probe that holds a key for `secs * 60`
   frames is only right at exactly 60 fps. Durations in tests must use the
   same clock the code uses.
4. **Check machine state** before bisecting a performance change: power mode or
   power limit (laptops cap GPU wattage in quiet modes), which display is
   primary (a USB or dock display can add frame time), thermal state, and
   other processes competing for CPU or GPU. A timing run gets the machine to
   itself.
5. **Check that the subject exists.** If scaling or changing the subject does
   not move the reading at all (it holds to four decimals), the instrument may
   be measuring something that is not there: culled geometry, a disabled
   feature, the wrong surface.
6. **Check the capture path.** Log diffs can differ only by text encoding
   (a console codepage turning an em dash into garbage). Read files with an
   explicit encoding and fold non-ASCII before hashing. Check that "before" logs
   contain nothing only the "after" code prints.
7. **Check the moment.** A correct-looking screenshot can be the wrong moment
   when the machine is loaded and game time drifts from wall time. Verify clocks
   or event markers, not just that the frame is non-blank.

Only after these: debug the code.

## Fix the instrument properly
- Make the test immune to the condition (use elapsed time, not frames), rather
  than pinning the condition (forcing a flag in CI) and leaving the trap armed.
- Add a note or check so the same mistake fails loudly next time.
- Report which suspect it was, with the evidence.

## Common Mistakes
| Mistake | What happens |
|---|---|
| Reverting the last commit because the gate went red | The real cause stays; a good change is lost |
| Adding retries to a "flaky" test | A deterministic instrument bug is hidden |
| Loosening the threshold | The gate stops guarding anything |
| Comparing with yesterday's log instead of the last pass | Chasing an unrelated difference |
| Running the benchmark while other work runs | Contention reads as regression |
