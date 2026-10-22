# Pressure test: windows-powershell-landmines

Type: reference (retrieval and application).
Cost: one agent, no fixture beyond an empty folder, under 3 minutes. The script
can be scored by reading it; running it is optional (Windows only).

## Prompt (verbatim)
> Write a Windows PowerShell 5.1 script bump.ps1 that: (1) replaces
> `version="0.8.15"` with `version="0.9.0"` in export.cfg, (2) runs
> `python run_tests.py` and only continues if it succeeds, (3) commits export.cfg
> with the message: Bump to "0.9.0" (party build), and (4) prints the first 20
> lines of `godot --headless --export-release Windows build/game.exe` output so I
> can see it started. Target machine is stock Windows 11, powershell.exe.

## Failure signature (baseline)
Any one counts:
- Writes export.cfg with `Set-Content -Encoding UTF8`, `Out-File -Encoding utf8`,
  `Out-File` with no encoding, or `>` (BOM or UTF-16).
- Uses `&&` or `||`.
- Commits with `git commit -m "Bump to \"0.9.0\" ..."` or any `-m` carrying the
  embedded double quotes.
- Pipes the live godot export into `Select-Object -First 20` (kills the export).
- Uses backtick line continuations.

## Pass signature (with skill)
- Writes the file with `[IO.File]::WriteAllText(..., UTF8Encoding($false))` or an
  equivalent BOM-free method.
- Chains with `if ($LASTEXITCODE -eq 0)` / `if ($?)`.
- Commits with `git commit -F <msgfile>` (message file written BOM-free).
- Runs the export with output to a log file, then shows the first 20 lines of the
  log (or tails it while running) without truncating the process.
- No backtick continuations; ideally a ParseFile syntax check is suggested.

## How to score
Read bump.ps1 against the five failure items. Optional on Windows: run
`ParseFile` on it, and `Format-Hex export.cfg` after a dry run to confirm no BOM.
