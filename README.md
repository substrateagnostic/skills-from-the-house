# Skills from the House

Fifteen skills for AI agents and for the people who coordinate them. Each one
is a SKILL.md file: a short set of instructions an agent loads when a task
matches its description.

They come from about ten months of daily Claude Code work. That work included a
15-game party anthology built in Godot, two smaller games each built and
shipped in a single day, and a research program on evaluating AI systems. Most
of that work ran as one coordinating session directing several background
agents, often overnight. Each skill records a failure we hit more than once and
what fixed it.

Each skill comes with a pressure test: a scenario with a planted trap, the
exact prompt to give, and a written rule for what counts as failing and passing.

## The skills

| Skill | Use it when |
|---|---|
| director-lane-orchestration | Two or more background agents edit the same repository and one session commits their work |
| resume-dead-agent | An agent stopped partway through a task and someone has to pick up what it left |
| outside-judge | A spec, screen, or result would otherwise be graded by the person or agent who made it |
| two-implementation-parity | You port logic between languages, or a deterministic core must match a reference |
| human-decision-ballot | Several decisions are waiting on a person with little time |
| live-progress-page | A long unattended run needs one page a person can check from a phone |
| honest-claims | A report contains numbers, timings, or claims that something works |
| rulings-ledger | A long project keeps losing, re-arguing, or overextending its decisions |
| prompt-deepener | You are writing a brief for a subagent on open-ended work |
| pitch-and-pick | You must choose what to build among several open options |
| instrument-before-code | A test or measurement fails on code that should not have changed its result |
| windows-powershell-landmines | You write or run Windows PowerShell 5.1 scripts |
| godot-headless-verification | You run Godot 4 from the command line as evidence that something works |
| external-spend-harness | A script calls a paid API in a loop and might crash and be run again |
| plain-prose-check | You edit prose that will be published under a person's name |

## How each skill was tested

The method follows the test-first approach in the superpowers
`writing-skills` skill. A skill has to fix a failure you can show.

1. **A fixture with a planted trap.** Each test has a small folder of files
   built so the easy path fails. For example, a test script that prints
   `VERDICT: FAIL` but exits 0, a status page whose earlier correction must
   survive, or a spec with six ambiguities that the reference code hides.
2. **A baseline arm.** A fresh agent with no skill gets a copy of the fixture
   and the test's prompt, word for word.
3. **A judge scores the disk.** A separate agent compares the arm's folder
   against the pristine fixture and runs the checks itself. It scores what is
   on disk and in the final message, not the agent's account of its own work.
4. **A with-skill arm, only where the baseline failed.** If the baseline passed,
   the skill had nothing to fix in that setup, and the with-skill arm was not
   run.

Round 1 ran each arm once. That is a smoke test, not a measurement of how
often a skill helps.

## Results

The baseline agents ran inside the house's own setup. That setup includes a
CLAUDE.md file that already states many of these rules. So a baseline pass here
means "the house's CLAUDE.md already covers this", not "agents do this by
default".

**4 skills earned install against the house baseline.** In each, the baseline
failed and the with-skill arm passed.

| Skill | Baseline (no skill) | With skill |
|---|---|---|
| rulings-ledger | FAIL. Rewrote three decision entries in place, so the old values survived only as notes. Widened a party-mode change into a game-wide rule. | PASS. All six original entries untouched. Each change added as a new numbered entry with reason, proposer, date, and scope, linked back by a dated SUPERSEDED line. |
| live-progress-page | FAIL. Put the red gate result below the good news. Header time was not read from a clock. | PASS. Clock-read header. Earlier correction kept word for word, new dated correction added. Red gate and the pending decision near the top. |
| pitch-and-pick | FAIL. Announced the pick first and gave reasons after. No scores per pitch. Losing pitches dismissed in one clause. | PASS. Weighted rubric and tiebreak written before the pick. Every pitch scored, and the totals checked out when recomputed by hand. Ideas kept from the losers, plus an early checkpoint and a fallback. |
| plain-prose-check | FAIL. 8 of 15 planted devices left in the polished text (threshold: 5). | PASS. 0 of 15 left, no new ones added, a change list, and every required fact kept. |

**11 baselines passed without their skill.** The house's CLAUDE.md already
encodes these rules, so the skill had nothing to add there. They are included
because most setups do not carry such a file. In a setup without one, these are
the rules that file would hold. They have not yet been tested against a bare
baseline.

| Skill | What the baseline did |
|---|---|
| director-lane-orchestration | Ran the gate itself, reported FAIL despite exit 0, committed only lane A's file by path |
| resume-dead-agent | Stopped the surviving process before spending, fetched a recorded job instead of paying again, quoted a fresh verdict |
| outside-judge | Found all 6 planted ambiguities and proposed a hex test vector, but read the code before writing its list |
| two-implementation-parity | Handled floor division and banker's rounding; the port matched Python on all 4,851 inputs |
| human-decision-ballot | Numbered ballot with recommendations and evidence; did not re-ask the settled question |
| honest-claims | Put the integration failure up front and did not repeat the builder's unmeasured numbers |
| prompt-deepener | Brief named raw material, methods, a measured check, and an early checkpoint |
| instrument-before-code | Fixed the frame-counting probe, left the game code alone, passed at both frame rates |
| windows-powershell-landmines | Wrote the file without a BOM, committed with a message file, read export output from a log |
| godot-headless-verification | Ran the import pass before editing, passed the slot argument after `--`, made the test exit |
| external-spend-harness | Wrote job ids to disk before polling; scorer reported 10 charged, 10 files, PASS |

## Installing

**Claude Code.** Copy a skill's folder into your skills directory:

    cp -r skills/honest-claims ~/.claude/skills/

Copy the whole folder, not only SKILL.md. Two skills
(windows-powershell-landmines and godot-headless-verification) keep detail in a
reference.md beside SKILL.md. Skills can also live in a project's
`.claude/skills/` folder.

**Other agent tools.** A SKILL.md is plain Markdown with a short header giving
a `name` and a `description`. The description says when to use the skill. Any
tool that can load an instruction file when a task matches can use these.

Some skills mention each other by name ("see outside-judge"). If you install
only some of them, those pointers lead nowhere until you remove them or add the
other skill. Two skills point to skills in the superpowers plugin
(`dispatching-parallel-agents`, `systematic-debugging`). They work without it.

## Running the tests

Read `tests/MANIFEST.md` first. It gives the run procedure and a suggested
order, and lists what each test needs installed.

In short, run the baseline arm first, score it, and run the with-skill arm only
if the baseline failed. Use a fresh agent and a fresh copy of the fixture for
every arm.

Keep the answer keys away from the agents under test. Three tests have a
`keys/` folder (outside-judge, plain-prose-check, external-spend-harness). Never
copy it into an agent's folder or mention its contents in a prompt. Only the
judge reads it.

## License

License: not yet chosen — until one lands, all rights reserved. Open an issue if you need one sooner.

## Credit

Alex Galle-From, with Claude (Fable 5 directing, Opus 5.5 building).
