---
name: windows-powershell-landmines
description: Use when writing, generating, or running Windows PowerShell 5.1 scripts or commands, when running git or native programs from PowerShell on Windows, when a PowerShell script fails to parse or reports an error far from the real cause, or when a file written from PowerShell breaks the program that reads it
---

# Windows PowerShell Landmines

## Overview
Windows PowerShell 5.1 (the `powershell.exe` that ships with Windows) differs
from PowerShell 7 and from bash in ways that fail quietly: files gain invisible
bytes, arguments get split or mangled, processes get killed by a pipeline.
Most of these produce no error at the point of the mistake.

Core principle: **assume 5.1 unless `$PSVersionTable.PSVersion` says otherwise,
and check the list below before writing files, passing arguments, or piping a
native program.**

## When to Use
- Generating a `.ps1` file or a one-line PowerShell command.
- Running git, Node, Python, Godot, or any `.exe` from PowerShell.
- A config file, `package.json`, or `.env` broke right after a PowerShell edit.
- A parse error points at code that looks fine.

## The short list (details and fixes in reference.md)
| Landmine | Safe pattern |
|---|---|
| `&&` and `\|\|` are parse errors in 5.1 | `cmd1; if ($?) { cmd2 }` |
| `Set-Content`/`Out-File -Encoding utf8` write a BOM | `[IO.File]::WriteAllText($p, $s, (New-Object Text.UTF8Encoding($false)))`, or edit with an editor tool |
| `>` and `Out-File` default to UTF-16 in 5.1 | Same as above; never `>` into a config file |
| `git commit -m` with embedded double quotes gets mangled | Write the message to a file; `git commit -F msg.txt` |
| Backtick line continuation breaks parsing, error reported far away | One long line, or build arguments in a variable |
| Piping a live native process into `Select-Object -First N` kills it | Redirect to a log file, then search the finished log |
| Native stdout decoded with the console codepage | Set `[Console]::OutputEncoding` to UTF-8, or read log files with an explicit encoding |
| `2>$null` hides errors a program prints to stderr | Capture `*>&1` to a log and read it |
| Stopping a background job leaves its child processes running | Check `Get-Process` / `tasklist` and stop children by PID |
| `$args` is automatic; using it as your own variable breaks | Name it something else |
| `Start-Process -ArgumentList "a b"` splits on spaces | Pass an array and quote paths with spaces |

## Before running a generated script
1. Syntax-check it without running:
   `$e=$null; [void][Management.Automation.Language.Parser]::ParseFile($path,[ref]$null,[ref]$e); $e`
2. If it reports an unbalanced brace you cannot see, search for backticks first.
3. Run native programs with output redirected to a file, then read the file.

## Common Mistakes
| Mistake | What happens |
|---|---|
| Bumping a version in a `.cfg` with `Set-Content -Encoding UTF8` | Reader sees a BOM and ignores the file or first key |
| `npm test && git commit` in 5.1 | Parse error, nothing runs |
| Commit message with `"quoted"` words via `-m` | Message truncated or split into pathspecs |
| `godot ... \| Select-Object -First 20` to peek | The run is killed after 20 lines |
| Treating `2>$null` output as clean | The script error went to stderr and was hidden |

See reference.md for each item's symptoms, exact fix, and the date it was last
confirmed.
