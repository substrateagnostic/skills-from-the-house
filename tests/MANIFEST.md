# Test manifest

Each skill has a pressure test in `tests/<skill>/test.md`. Paths inside a
test.md are relative to that test's folder, so `fixture/` in
`tests/honest-claims/test.md` means `tests/honest-claims/fixture/`.

## Folder layout

- `test.md` is the scenario: setup, the exact prompt, the failure signature,
  the pass signature, and how to score.
- `fixture/` holds the files the test agent works on. Copy it into a fresh
  folder for each arm so the original stays clean.
- `keys/` holds answer keys and scorers. Three tests have one:
  outside-judge, plain-prose-check, and external-spend-harness. Test agents must
  never see these files. Keep them outside the agent's folder and read them
  only when scoring.

Two tests (prompt-deepener, windows-powershell-landmines) need no fixture. The
agent starts in an empty folder.

## How to run a test

1. **Baseline arm.** Start a fresh agent with no skill installed. Copy
   `fixture/` into a new folder, set that as its working directory, and give it
   the prompt from test.md word for word. Record the commands it ran and its
   final message.
2. **Score the baseline** against the failure signature, using the disk state
   the agent left behind, not its description of what it did.
3. **If the baseline did not fail, stop.** The skill has nothing to fix for that
   scenario in your setup. Record that result.
4. **Skill arm.** Only if the baseline failed: start a fresh agent with the
   SKILL.md (and reference.md, if the skill has one) installed or pasted in as
   context. Use a new copy of the fixture and the same prompt.
5. **Score the skill arm** against the pass signature.

One run per arm is a smoke test, not proof. For a skill that passes narrowly,
or when you are testing a change to its wording, run five or more times per
arm.

The judge should be a separate agent or person from the one that ran the arm.
Give the judge the test.md, the pristine fixture, the arm's folder, and the key
if there is one.

## Suggested order

Cheap, broadly useful tests come first so early results calibrate the rest.

1. honest-claims
2. director-lane-orchestration
3. resume-dead-agent
4. outside-judge
5. instrument-before-code
6. prompt-deepener
7. rulings-ledger
8. two-implementation-parity
9. plain-prose-check
10. human-decision-ballot, then live-progress-page (it refers to both
    human-decision-ballot and honest-claims)
11. pitch-and-pick
12. The reference skills: windows-powershell-landmines,
    godot-headless-verification, external-spend-harness

## The set

| # | Skill | Scenario | Needs | Fixture checked before any agent ran |
|---|---|---|---|---|
| 1 | director-lane-orchestration | Commit lane A's work while lane B's half-done file is staged and the gate exits 0 on FAIL | bash, git, python | setup.sh run once: prints VERDICT FAIL, exits 0, text_b.py staged |
| 2 | resume-dead-agent | Finish a dead agent's paid batch: a surviving process, a stale lane doc, recorded job ids | bash, python | read through |
| 3 | outside-judge | Judge a binary-format spec for hand-off while the reference code sits beside it; 6 planted ambiguities | python (optional) | example length checked: 23 bytes |
| 4 | two-implementation-parity | Port a Python scoring function to JS; floor division of negatives and banker's rounding planted | python, node | traps confirmed (Python -2 and 2 where JS gives -1 and 3) |
| 5 | human-decision-ballot | Morning message from overnight notes with 5 decisions, 1 already settled, 1 trivial | nothing | read through |
| 6 | live-progress-page | Edition 3 of a progress page: keep the old correction, add a new one, surface a red gate | nothing | read through |
| 7 | honest-claims | Group-chat status from a cheerful builder report against logs with a FAIL at exit 0 | nothing | read through |
| 8 | rulings-ledger | Record three owner decisions that supersede entries whose neighbors share anchor text | nothing | read through |
| 9 | prompt-deepener | Brief a subagent to "make the night sky look right" | nothing | no fixture |
| 10 | pitch-and-pick | Pick among three game-jam pitches | nothing | read through |
| 11 | instrument-before-code | A "docs-only" commit broke a gate; the real cause is a frames-as-seconds probe and a dropped flag | python | both runs confirmed: FAIL free-running, PASS at fixed fps |
| 12 | windows-powershell-landmines | Write bump.ps1: a config edit, a gated commit with a quoted message, a peek at export output | nothing (Windows to run it) | no fixture |
| 13 | godot-headless-verification | New class_name "not declared"; the test never exits; an autoload grabs the real save slot | Godot 4.x on PATH | confirmed on Godot 4.6.2 |
| 14 | external-spend-harness | Write a paid-batch script against a local stub; the director crashes it after job 4 and runs it again | python | a ledger-first harness scores 10 charged / 10 files (PASS); a naive one 14 charged / 1 file (FAIL) |
| 15 | plain-prose-check | Polish a mannered About-page draft with 14 to 15 planted devices | nothing | read through |

"Read through" means the fixture was written and read, but no script was run
against it before the first agent arm.

## Known limits of these tests

- **pitch-and-pick** supplies the pitches, so step 2 of the skill (getting
  independent pitches) is not exercised. A full test needs sub-agents.
- **live-progress-page** overlaps with honest-claims and human-decision-ballot.
  A pass may come from those habits rather than this skill.
- **prompt-deepener** is scored against a rubric by a judge, not by a script.
- **godot-headless-verification** needs Godot installed for the full test.
  Without it, score the agent's commands and edits only.
