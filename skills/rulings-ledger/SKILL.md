---
name: rulings-ledger
description: Use when a multi-session or multi-agent project keeps relitigating or forgetting its decisions, when agents cite an old rule as if it applied everywhere, when starting a project or sprint that needs a written set of binding decisions, when a new request conflicts with an earlier decision, or when editing any append-only record such as a decisions log, changelog, or constitution
---

# Rulings Ledger

## Overview
Projects that run across many sessions or agents need their decisions written
down in one place, numbered, with the reason each was made and how far it
reaches. Without that, decisions get re-argued, forgotten, or stretched past
the situation they were made for.

Core principle: **each decision is a numbered entry with its reason and its
scope; later changes are added under it, and the original text stays.**

## When to Use
- Work spans sessions or agents and decisions keep getting lost or re-argued.
- Someone cites "the rule" and nobody can say where it came from.
- A new request from the owner contradicts something decided earlier.
- You are about to edit a decisions log, changelog, or any record where
  entries must never be lost.

## Entry format
```
## R7. Max players is 4
Decision: The game supports at most 4 local players.
Proposed by: owner, 2026-10-14
Reason: couch has 4 controllers; 5-player HUD measured unreadable (shots/hud5.png)
Scope: LANE-SCOPED (local party mode only)
```
Scope tags, set when the entry is written:
- **GENERAL**: applies to the whole project.
- **LANE-SCOPED**: applies to one feature, mode, or piece of work. Name it.
- **OWNER-TASTE**: a preference; cheap to overrule.
- **STALE-CANDIDATE**: may no longer apply; flagged for review.

## Changing a decision
- Add a line under the entry, never rewrite it:
  ```
  NARROWED 2026-10-20: applies to 4:3 displays only (owner).
  SUPERSEDED 2026-10-21 BY R12: owner asked for 6 players in party mode.
  ```
- The new decision gets its own entry with its own reason and scope, and links
  back to the one it replaces.
- Entries stay in the order they were made. Numbers are never reused.

## How decisions bind
1. **Decisions can be replaced.** Taste calls are cheap to overrule.
   Verification rules (how something is tested or proven) change only with a
   stated reason, because loosening them hides failures.
2. **When the owner asks for something that conflicts with an entry**, build
   what they asked at full strength, and add a one-line note naming the entry
   it conflicts with. Do not refuse or water it down because of the old entry.
3. **Briefs cite entry numbers** ("per R7") instead of copying values, so a
   superseded value cannot survive in an old brief.
4. **When a brief and the shipping code disagree**, the code is the fact; fix
   the brief and, if needed, add a ledger entry.
5. **Review scopes now and then.** Entries tagged GENERAL that were really about
   one feature are the main source of wrong rules. Re-tag them, with a dated
   note.

## Editing the ledger safely
String-replace edit tools can delete a neighbor when the anchor text is
too short or shared between entries.
1. **Before editing, list every entry ID**: `grep -c "^## R" LEDGER.md` and save
   the list (`grep "^## R" LEDGER.md > /tmp/ids_before`).
2. **Pick an anchor that includes the whole line you are inserting after**, and
   put that line back in your replacement text unchanged.
3. **Append under an entry**, not inside another entry's text.
4. **After editing, list the IDs again and compare**: same IDs plus your new
   ones, none missing. If an entry vanished, restore it before anything else.
5. **If an entry records a command and its result**, changing the command means
   re-running it and recording the new result in the same edit.

## Common Mistakes
| Mistake | Fix |
|---|---|
| Editing the old entry's text to the new value | Add SUPERSEDED under it; new entry for the new value |
| No scope tag | Every entry gets one at birth |
| Arguing with the owner using an old entry | Build what they asked; note the conflict |
| Briefs that copy values | Cite the entry number |
| Not checking IDs after an edit | Before/after ID list, every time |
