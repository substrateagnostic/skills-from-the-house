---
name: resume-dead-agent
description: Use when a background agent or subagent ended without a final report, when a session hit its limit or was killed partway through a task, when a workflow shows failed but files changed anyway, or when picking up another session's uncommitted work
---

# Resume a Dead Agent

## Overview
An agent that stopped is not the same as work that stopped. Its files, logs,
child processes, and paid jobs may all still be there, some still running.
Re-dispatching the original brief from scratch redoes finished work, can spend
money twice, and can overwrite what survived.

Core principle: **inventory what exists before you act, and assume the dead
agent's processes may still be alive.**

## When to Use
- A background agent's task ended with no report or a truncated one.
- A session was killed, hit a usage limit, or crashed mid-task.
- A tool says "failed" but `git status` shows changes.
- You are a new session inheriting someone else's uncommitted tree.

## Steps, in order
1. **Look for survivors first.** List processes the dead agent may have
   started (`tasklist /v`, `Get-CimInstance Win32_Process | select ProcessId,CommandLine`,
   `ps aux`). Match on command line, not just process name. On Windows,
   stopping a shell does not stop its children. A surviving harness can keep
   writing files and calling paid APIs. Decide per survivor: let it finish, or
   stop it by PID. Do nothing else until this is settled.
2. **Inventory.** Record, in a scratch note:
   - `git status` and `git diff --stat` (what changed, staged or not)
   - the agent's plan or lane doc checklist (what it said it would do)
   - its output folder (what evidence exists, with timestamps)
   - the tail of its logs (last thing it did)
   - any job ledger for external calls (job ids already submitted)
3. **Read the transcript.** Session transcripts usually survive the session.
   Read the dead agent's last messages instead of guessing what it was doing.
4. **Mark each checklist item** done-and-verified, done-but-unverified, partly
   done, or not started. A log without a final verdict line counts as
   unverified, never as passed.
5. **Try one resume.** If the agent can be messaged, send ONE message with
   explicit instructions: what is already done, what remains, "poll long jobs
   inside a foreground call, do not end your turn to wait." If it does not
   recover, stop it.
6. **Otherwise start a continuation agent** briefed from your inventory, not
   the original prompt. Tell it which items are finished, which files not to
   touch, and which job ids must never be re-submitted.
7. **Re-run lost verification.** Any check whose verdict was not captured is
   run again, on the current tree, before anything is committed.
8. **Never re-fire a recorded external job.** If a job id is in the ledger,
   fetch its result; do not submit it again. If there is no ledger, list the
   provider's recent jobs before submitting anything.

## Quick Reference
| You see | Do |
|---|---|
| Log ends mid-run, no verdict | Re-run the check |
| Files changed, no report | Inventory, then decide; do not revert by reflex |
| Harness process still alive | Settle it (wait or kill by PID) before anything else |
| Job ids recorded, results missing | Fetch results by id; never resubmit |
| "Before" logs newer than the code change | Grep them for after-only output; a survivor may have overwritten them |

## Common Mistakes
| Mistake | What happens |
|---|---|
| Re-dispatching the original brief | Finished work redone; survivors overwritten |
| Killing processes by name to "clean up" | Kills other agents' live runs |
| Trusting the dead agent's last "it passes" | That line was never confirmed by a verdict |
| Reverting the dead agent's changes unread | Throws away work that was finished |
| Re-submitting paid jobs because results aren't on disk | Pays twice; the first batch may land a minute later |
