---
name: godot-headless-verification
description: Use when running Godot 4 from the command line or headless for tests, captures, exports, or verification; when a Godot parse or type error appears right after adding a script or class_name; when a headless Godot run hangs, crashes at exit, or gives different results between runs; or when an agent must verify Godot work without the editor open
---

# Godot Headless Verification

## Overview
Godot's command line behaves differently from the editor in ways that make
checks lie: new classes are invisible until an import pass, game arguments get
eaten by the engine, runs never exit, and results drift with frame rate. Most
of these look like code bugs and are not.

Core principle: **before trusting a headless Godot verdict, confirm the import
cache is fresh, the arguments reached the game, the run was bounded, and the
timing was fixed.**

## When to Use
- Any `godot --headless` run used as evidence (tests, captures, exports).
- "Identifier X not declared" or "Could not find type X" right after adding a
  script.
- A headless run that never finishes, or segfaults at exit.
- Results that differ between two runs of the same tree.

## Checklist
1. **Import pass after adding or renaming any script with `class_name`**:
   `godot --headless --editor --import --quit --path .`
   Global classes come from `.godot/global_script_class_cache.cfg`; a plain run
   does not rebuild it. The error usually names the consumer, not the new file.
2. **Game arguments go after `--`**:
   `godot --headless --path . res://main.tscn -- --slot=3 --mytest`
   Anything before `--` is parsed by the engine and may be dropped. Read them
   with `OS.get_cmdline_user_args()`.
3. **Bound every run.** Use `--quit-after <frames>` or a project-specific quit
   flag. A standalone scene that never calls `get_tree().quit()` runs forever at
   full CPU, and log collection that waits for exit hangs with it.
4. **Fix the timestep for determinism**: `--fixed-fps 60`. Free-running
   headless runs go as fast as the CPU allows, so anything counting frames
   instead of seconds changes meaning between machines.
5. **Paths given to the game are usually project-relative.** If a script treats
   an output path as `res://`-relative, an absolute Windows path silently
   produces nothing. Check the first output file exists.
6. **Read the verdict line, not the exit code.** Many projects' test scripts
   exit 0 on failure, and some Godot runs crash at shutdown after a valid run
   (see reference.md for telling a harmless exit crash from a real one).
7. **Capture all output to a log, then read it.** Godot prints script errors to
   stderr. Do not pipe a live run into a line-limiting command.
8. **One windowed or GPU-heavy Godot at a time**, launched and stopped by
   recorded PID. Never stop all Godot processes by name.
9. **Protect user data.** If the game autoloads a save or config on boot, every
   test run (including parse checks and import passes) points at a scratch slot
   or a copy of `user://`.
10. **Sandboxed agents may not be able to run Godot at all** (no GPU, no
    display, blocked binaries). Brief them for the edit; a session that can run
    Godot does the verification.

## Common Mistakes
| Mistake | Fix |
|---|---|
| Editing code to fix "not declared" after adding a class | Run the import pass first |
| `godot --slot=3 --path . scene.tscn` | `godot --path . scene.tscn -- --slot=3` |
| Boot smoke passes, so the feature works | Smoke a path that actually loads the new code |
| Unbounded headless run in a loop | `--quit-after` or a quit flag |
| Calling a frame-count probe "flaky" | `--fixed-fps 60`, or measure in seconds |

Engine-behavior traps that look like code or art bugs (transforms before
`_ready`, SurfaceTool normals, light angles, preload cycles) are in
reference.md.
