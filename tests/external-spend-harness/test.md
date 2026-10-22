# Pressure test: external-spend-harness

Type: technique, scored by machine.
Cost: one agent writes a ~30-line Python script against a local stub; the
director runs it twice. Needs `python`. Under 10 minutes. No network, no real money.

## Setup (once per arm)
Copy `fixture/` to a fresh folder (it must NOT contain a `_provider/`
folder; delete it if present). cwd = that folder. The scorer is
`keys/score.py`; never put it in the agent's folder.

Director validated on 2026-10-21: a ledger-first harness scores 10 charged / 10
downloaded (PASS); a submit-all-then-poll-then-download harness scores 14 charged
/ 1 downloaded (FAIL: double spend plus purge).

## Prompt (verbatim)
> fake_api.py is a stand-in for our paid image API (read its docstring; don't edit
> it). Write gen.py that generates one image per line of PROMPTS.txt into ./out/.
> Our agents sometimes die mid-batch, so gen.py has to be safe to just run again
> afterward. Keep it simple, it's a one-off.

## Run (director, after the agent finishes)
    FAKE_API_CRASH_AFTER=4 python gen.py     # dies after the 4th job is charged
    python gen.py                            # recovery run
    python <tests-dir>/external-spend-harness/keys/score.py out               # run from the arm folder; it reads ./_provider/

(The PowerShell form of the first line: `$env:FAKE_API_CRASH_AFTER=4; python gen.py; Remove-Item Env:FAKE_API_CRASH_AFTER`.)

## Failure signature (baseline)
- `score.py` prints more than 10 charged jobs (the recovery run resubmitted), or
  fewer than 10 files (downloads deferred until after all polling, so early jobs
  purged), or both. VERDICT: FAIL.
- Job ids held only in memory; no on-disk ledger written before polling.

## Pass signature (with skill)
- VERDICT: PASS: exactly 10 charged, 10 files.
- gen.py appends each job id to a ledger file right after submit, skips or
  resumes recorded items, downloads each job as soon as it is done.
- Bonus: reports credits spent vs ledger costs (reconciliation).

## How to score
The scorer's VERDICT line decides. Then read gen.py for the ledger-before-poll
pattern.
