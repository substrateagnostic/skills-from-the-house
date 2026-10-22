---
name: external-spend-harness
description: Use when writing or running scripts that call paid generation or batch APIs (3D models, images, audio, video, LLM batch jobs) from an agent, when a paid job batch crashed or was interrupted and might be re-run, when generated assets expire on the provider's side, or when credits spent do not match what was expected
---

# External Spend Harness

## Overview
Agents that call paid APIs fail in expensive ways: a crash and a naive re-run
pays twice, a dead agent's script keeps spending, results expire on the
provider before anyone downloads them, and nobody can say where the credits
went. A small amount of bookkeeping prevents all of it.

Core principle: **record every job id the moment it exists, never submit a
recorded job again, download as soon as a job finishes, and reconcile the
credits.**

## When to Use
- Any script that submits paid jobs in a loop.
- Re-running a batch after a crash, timeout, or killed agent.
- Providers that delete results after a few days.
- Several agents or scripts sharing one account balance.

## Harness rules
1. **Write the ledger before polling.** Append `{item, job_id, submitted_at,
   cost}` to a local append-only file (JSON lines) immediately after the
   submit call returns, before waiting on anything. A crash after submit must
   still leave the id on disk.
2. **Dedupe on re-run.** Before submitting an item, check the ledger. If it has
   a job id, poll or download that job instead. Never resubmit an item with a
   recorded id unless the job is confirmed failed by the provider, and record
   that failure.
3. **Check for survivors before any re-run.** A previous run's process may still
   be alive and submitting (see resume-dead-agent). List processes by command
   line first.
4. **Download on completion, same session.** Pull every finished asset to local
   disk right away and record the local path and file hash in the ledger.
   Providers purge results; a "finished" job you never downloaded is a paid-for
   loss.
5. **Reconcile.** At the end, compare: credits before minus credits after,
   against the sum of costs in the ledger. Report any difference. With several
   scripts sharing an account, the balance delta is not your spend; audit by
   job ids instead.
6. **Make crashes cheap.** The harness should be safe to run again with no
   arguments and pick up where it left off.
7. **Separate generation from adoption.** Generating can be pre-approved within
   a budget; choosing which outputs go into the product goes to a person or an
   outside judge (see outside-judge).
8. **Keep the style or spec paragraph identical across prompts.** Paste the
   same paragraph into every prompt in a batch so results are comparable, and
   store it in the ledger header.
9. **Respect provider limits** (rate limits, concurrency caps, prompt length).
   A provider can silently truncate a long prompt; measure its real limit once
   and record it.

## Ledger line example
```json
{"item":"lamp_03","job_id":"tsk_81f2","submitted_at":"2026-10-21T22:14:05","cost":15,"status":"downloaded","path":"assets_raw/lamp_03.glb","sha256":"9c1e..."}
```

## Common Mistakes
| Mistake | What happens |
|---|---|
| Job ids kept only in memory until the batch ends | Crash loses them; re-run pays again |
| Re-running "from the top" after a failure | Every finished job is bought twice |
| Downloading "tomorrow" | Assets purged; credits lost |
| Reading the account balance change as this script's cost | Other scripts' spend gets blamed or hidden |
| Agent picks its own favorites into the product | No outside check on quality |
