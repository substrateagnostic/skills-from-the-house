---
name: live-progress-page
description: Use when running an overnight or multi-hour autonomous session that a person will check in on, when a reviewer will look at progress from a phone, when most of the evidence is images or screenshots, or when updating a status page or document that earlier editions already published
---

# Live Progress Page

## Overview
During a long unattended run, the person should be able to look at one place,
at any moment, and see what was done, what was found, what was not checked,
and what needs them. One page at one stable address, updated in place, beats
a stream of chat messages they have to scroll back through.

Core principle: **one page, one address, updated in place; every claim points
to its evidence; mistakes stay on the page.**

## When to Use
- A run of more than an hour or two with nobody watching.
- The reviewer checks in from a phone or between other work.
- Evidence is mostly visual (screenshots, renders, charts).

Needs some way to publish a page at a stable address (a hosted page or
artifact tool, a shared doc, a file in a synced folder). If none exists, use a
single file at a fixed path in the repo and tell the person that path once.

## Page layout, top to bottom
1. **Header line**: edition number and the time read from the clock
   ("Edition 4, 03:12"). Run `date`; never estimate.
2. **Needs you**: decisions as a ballot (see human-decision-ballot). Empty
   section says "nothing needed".
3. **Done since last edition**: each item with the path or link to its
   evidence, and the verdict line if a test was run.
4. **Findings**: what the work discovered, each tagged measured or inferred
   (see honest-claims).
5. **Not shown / not checked**: what this run did not verify, could not see,
   or skipped. Never empty by default; write "none known" only after looking.
6. **In flight**: what is running now and when it should finish.
7. **What I got wrong**: corrections to earlier editions, dated. This section
   is kept and only grows. Never delete or rewrite an entry.

## Rules
1. **Republish to the same address.** A new address each time means the person
   has to find the newest one.
2. **Carry forward, don't restart.** Each edition starts from the last one.
   Done items can be condensed, but "What I got wrong" entries are copied
   whole.
3. **Images: pairs and sheets.** Show before and after side by side, or a
   contact sheet, with a one-line caption saying what to look at. Avoid dumps
   of many near-identical frames.
4. **The coordinator publishes.** If subagents produce images, they save them
   to their output folders; the coordinating session puts them on the page.
   Subagent send or upload calls can report success without reaching anyone.
5. **Update at milestones**, not on a timer: a gate passed or failed, a
   decision needed, a surprise found.
6. **Push a short ping when the page changes in a way that needs the person**
   (a new decision, a red result). Otherwise let the page carry it.

## Common Mistakes
| Mistake | Fix |
|---|---|
| New page or new message each update | One address, republished |
| "Fixed the lighting" with no picture | Before/after pair, path cited |
| Dropping last edition's correction | Corrections section only grows |
| No "not checked" section | Always present; look before writing "none known" |
| Timestamps typed from memory | Read the clock each edition |
