# Windows PowerShell 5.1 landmines: reference

Each entry: symptom, cause, fix, last confirmed. "Last confirmed" is the date the
problem was hit and fixed in real work; behavior can change with harness or
Windows updates, so re-test anything older than a few months before relying on it.

## Chaining commands
- Symptom: `The token '&&' is not a valid statement separator in this version.`
- Cause: `&&` and `||` arrived in PowerShell 7.
- Fix: `cmd1; if ($?) { cmd2 }`. For native programs, `$LASTEXITCODE -eq 0` is
  more reliable than `$?`.
- Last confirmed: 2026 (standing harness note).

## File encoding
- Symptom: a `.cfg`, `.ini`, `package.json`, or `.env` stops being read
  correctly after a PowerShell edit. Godot found zero export presets; Node's
  `process.loadEnvFile` silently corrupted the first key; JSON parsers fail at
  position 0.
- Cause: in 5.1, `Set-Content -Encoding UTF8` and `Out-File -Encoding utf8` write
  a UTF-8 byte order mark (BOM). `>` and `Out-File` without `-Encoding` write
  UTF-16 LE.
- Fix: `[IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($false)))`.
  Or use an editor tool that preserves encoding. To check a file:
  `Format-Hex $path | Select-Object -First 1` (a BOM shows as `EF BB BF`).
- Last confirmed: 2026-08-07 (.cfg), 2026-07-21 (.env, package.json).

## git commit messages
- Symptom: commit message truncated, or git reports pathspec errors for words of
  the message.
- Cause: 5.1 passes arguments to native programs with broken quoting when the
  string contains double quotes (including inside here-strings).
- Fix: write the message to a file and use `git commit -F msgfile`. In a bash
  tool, a heredoc into a file works well.
- Last confirmed: 2026-09 (repeat occurrences 2026-07-04 onward).

## Backtick line continuation
- Symptom: `Missing closing '}' in statement block` pointing at a function whose
  braces are balanced, often dozens of lines from the real problem.
- Cause: a backtick continuation followed by trailing whitespace or a line
  ending the parser does not expect.
- Fix: never generate backtick continuations. Put the command on one line, or
  collect parameters in a hashtable and splat: `$p=@{FilePath='x';PassThru=$true}; Start-Process @p`.
- Check: `[Management.Automation.Language.Parser]::ParseFile($path,[ref]$null,[ref]$errs)`.
- Last confirmed: 2026-08-13.

## Pipelines that kill native processes
- Symptom: a long native run (export, build, game) exits with 255 or stops
  mid-way exactly when output reached N lines.
- Cause: `| Select-Object -First N` stops the pipeline after N items and
  PowerShell terminates the upstream native process.
- Fix: `& prog args *>&1 | Out-File -Encoding utf8 run.log`, wait for it to
  finish, then search `run.log`.
- Also: searching output for "error" matches filenames like `error_005.wav`;
  match the program's real error prefix.
- Last confirmed: 2026-07 (a Godot game's export pipeline).

## Console codepage and captured output
- Symptom: two logs of the same program differ only by characters like an em
  dash turning into `ΓÇö`.
- Cause: PowerShell decodes a native program's stdout using
  `[Console]::OutputEncoding`, which follows the console codepage, not UTF-8.
  Two shells with different codepages produce different files from the same
  output.
- Fix: set `[Console]::OutputEncoding = [Text.Encoding]::UTF8` before running,
  read logs with an explicit `-Encoding`, and fold non-ASCII before hashing
  logs for comparison (`-replace '[^\x20-\x7E]+','?'`).
- Last confirmed: 2026-08-13.

## stderr suppression
- Symptom: a run "has no errors" but the program did fail.
- Cause: many programs (Godot included) print script errors to stderr;
  `2>$null` throws them away. In 5.1, redirecting native stderr with `2>&1`
  also wraps lines as error records and can set `$?` false on success.
- Fix: capture everything to a log with `*>&1 | Out-File` and read it.
- Last confirmed: 2026-07.

## Background jobs and child processes
- Symptom: after stopping a background task, files keep changing or logs keep
  growing; a paid API keeps getting called.
- Cause: on Windows, stopping a shell or job does not stop the processes it
  started.
- Fix: list processes with their command lines,
  `Get-CimInstance Win32_Process | Where-Object CommandLine -like '*name*' | Select ProcessId,CommandLine`,
  and stop the specific PIDs. Never stop all processes by name; another agent's
  run may be one of them.
- Last confirmed: 2026-07-07, 2026-09-04.

## Automatic variables
- `$args`, `$input`, `$_`, `$PSItem`, `$Matches`, `$Error`, `$Host`, `$PID`,
  `$PWD` are automatic. Assigning your own value to `$args` or `$input` breaks
  silently. Use other names.
- Last confirmed: general PowerShell behavior.

## Start-Process arguments
- Symptom: a program receives a path split at its spaces.
- Cause: `-ArgumentList` joins an array with spaces and does not quote elements.
- Fix: quote elements that contain spaces yourself:
  `-ArgumentList '--path', '"C:\My Folder\x"'`.
- Last confirmed: general 5.1 behavior.

## Reported, not re-verified
- Long-running background shell tasks with no output for a long time have been
  reported to be stopped by agent harnesses; printing a short heartbeat line
  every ~25 seconds avoided it. Source is a working note, not a reproduced test.
  Treat as a hint.
