---
name: director-lane-orchestration
description: Use when coordinating two or more background agents that edit files in the same repository, when running a long or overnight autonomous session with builder subagents, or when acting as the single coordinator who commits other agents' work
---

# Director and Lanes

## Overview
One session (the director) coordinates. Each background agent (a lane) owns a
declared set of files and an output folder. Lanes edit and measure. The
director checks, commits, and talks to the human. The goal is a shared working
tree that stays correct while several agents touch it at once.

Core principle: **an agent's report is a claim, not a fact. The director
re-checks every claim that matters before committing it or passing it on.**

## When to Use
- Two or more agents will edit the same repo at the same time.
- A run will last hours with nobody watching.
- Some agents cannot run the tests or write to git (sandboxed models, other
  vendors' CLIs) and someone must check their work.

Not needed for one agent doing one task, or for read-only research fan-out
(superpowers:dispatching-parallel-agents covers that).

## The lane doc (the lane writes it BEFORE its first edit)
Path: `agents/<lane-name>-lane.md` in the repo, or wherever the project keeps
them. Template:

    # <LANE NAME> (<model>), DECLARED <date and time read from the clock>, base <commit sha>
    Binding: <rules documents and entry IDs this lane follows>
    ## Invariant: <the one thing this lane must not change, and how it proves it didn't>
    ## Baseline (measured before any edit): <the test or gate result now>
    ## Design calls (declared before the edits): <each decision and why>
    ## Will create: <paths>
    ## Will edit: <paths>
    ## Will NOT edit: <paths other lanes own>
    ## Mid-lane additions: <scope changes, each with who approved it>
    ## Status: <checklist, updated as items land>
    ## Resume: <exact commands to re-run its checks, for whoever picks this up>

The director reads the declaration before the lane edits, and resolves any
overlap between two lanes' "will edit" lists before either starts.

## Rules for lanes (put these in every brief)
1. **No git writes.** No commit, stash, reset, or checkout of other files.
   The director commits.
2. **Evidence goes only in your own output folder** (for example
   `verify_out/<lane>/`). Never write into another lane's folder or a shared
   results folder. Give each phase (before, after) its own subfolder so a rerun
   cannot overwrite earlier evidence.
3. **Depend only on committed code.** If you need a helper from a file another
   lane is editing, copy the lines into your own file with a comment saying
   where they came from, or wait for the commit.
4. **Exclusive resources one at a time** (a GPU, a game window, a timing
   measurement, a paid API). Record the PID you launch. Kill only that PID. A
   cleanup that cannot name its target is not allowed.
5. **Never end your turn to wait for a background job.** Nothing wakes you up
   again. Poll long jobs inside a foreground call, and finish your report in
   this run.
6. **Stage files, don't send them.** Files meant for the human go in your output
   folder with a manifest line in your report. The director sends them.
   (Subagent file-send calls can return success without reaching the user.)
7. **Quote the verdict line, not a summary of it.** Paste the actual PASS/FAIL
   line and the log path. A failure is the first line of the report.

## Rules for the director
1. **Commit by pathspec** (`git commit -F msgfile -- <paths>`). Never run a bare
   `git commit` after `git add`: it sweeps in other lanes' staged files.
2. **Read the verdict, not the exit code.** Many scripts exit 0 on FAIL. Never
   chain a commit after a test with `&&`.
3. **Run what the lane could not.** If a lane's sandbox cannot run the tests or
   git, brief it for the edit only, run the full check yourself, and say in the
   commit message that the lane did not check it. Do not re-dispatch a lane for
   failing to run something it never could.
4. **Verify side effects yourself.** "Pushed", "sent", "uploaded", "fired N
   jobs": confirm with your own read (git log, a list call, the provider's API)
   before passing it on.
5. **No `git stash` on a shared tree.** It takes every lane's uncommitted work.
   For an A/B comparison, copy your files to a scratch folder or worktree.
6. **Measure a tree that other lanes are mid-edit on** in a scratch copy with
   their files pinned to HEAD, not by temporarily reverting the shared tree.
7. **Keep evidence tied to the code it measured.** Store results under the
   commit sha they came from. Before trusting a "before" log, grep it for
   strings only the "after" code prints.
8. **Leave a committed, runnable state at every boundary.** Before a usage
   window ends, a session limit, or a handoff: commit what passes, write the
   next step in a repo file, leave no half-applied edits.
9. **Mirror the task list into the repo** (for example `docs/BOARD.md`). Harness
   task boards belong to the session or account and can vanish on resume or a
   login change.
10. **Get an outside check** on anything the lanes would otherwise grade
    themselves (see outside-judge).

## When a lane dies
Use resume-dead-agent. Do not re-dispatch the same brief until you have
inventoried what the dead lane left behind.

## Common Mistakes
| Mistake | What happens | Fix |
|---|---|---|
| Lane told "commit each step" in a no-git sandbox | Work sits uncommitted and is lost | Brief for the edit; director commits |
| Two lanes kill "all python/godot processes" | One kills the other's live run | Kill by recorded PID only |
| Lane ends its turn "waiting for the build" | Lane is dead; no report | Poll inside a foreground call |
| Director trusts "sent to user" from a subagent | User never got it | Director sends; lanes stage |
| Timing run launched in the same turn as other work | Contended numbers read as regressions | A measurement gets the machine to itself |
| Brief quotes a constant from memory | Lane follows a stale value | Cite the source file and sha in the same line |
| `git add -A && git commit` after a lane reports done | Another lane's half-done files ship | Pathspec commit of the reporting lane's paths |
