# Godot 4 verification: reference

Each entry: symptom, cause, fix, last confirmed (Godot 4.x, Windows 11 unless
noted). Re-test older entries after an engine upgrade.

## Import cache and class_name
- Symptom: `Identifier "Foo" not declared in the current scope` or `Could not
  find type "Foo"` in a script that uses a class you just added. Boot smoke may
  still pass because the boot scene never loads the consumer.
- Cause: global classes resolve from `.godot/global_script_class_cache.cfg`,
  rebuilt only by an editor import pass.
- Fix: `godot --headless --editor --import --quit --path .`, then smoke a path
  that loads the new code (not just the boot scene).
- Last confirmed: 2026-07-07 and 2026-08-13.

## Preload cycles
- Symptom: two scripts both fail to parse; the error names only one.
- Cause: A preloads B, and B references A's class or constants.
- Fix: a preloaded script must not reference its preloader. Move the shared
  constant into the preloaded file.
- Last confirmed: 2026-08-13.

## .import files after reimport
- Symptom: after reverting `*.import` files, the project boots to nothing,
  silently.
- Cause: changed source assets get new `.import` metadata that is real; reverting
  it desyncs the `.godot` cache.
- Fix: revert only `.import` churn for sources you did not change. Run checks
  after any import or revert, never between.
- Last confirmed: 2026-07-31.

## Exit crashes
- Symptom: a windowed or probe run prints all its results, then exits with
  signal 11 / code 139 / -1, sometimes with a modal Windows "Application Error"
  dialog.
- Telling harmless from real: harmless if every expected result line and the
  verdict printed BEFORE the crash and the crash is in shutdown. Real if output
  stops mid-run or the verdict is missing.
- Cleanup: the modal dialog can leave Godot processes behind. After the run,
  list Godot processes by PID and stop the ones you launched.
- Last confirmed: 2026-07-22 (project-specific pre-existing crash; check your
  own project's history before assuming it is harmless).

## Frame rate and time
- Free-running headless runs go as fast as the CPU allows (often 140+ fps on a
  desktop). Windowed runs follow the display's refresh rate with vsync.
- Probes that count frames (hold a key for N frames, capture at frame N) only
  mean seconds at a fixed rate. Use `--fixed-fps 60` or accumulate the same
  delta time the game uses.
- Fixed-step runs hash identical between runs; free-running windowed runs can
  differ from themselves.
- Last confirmed: 2026-08-13, 2026-08-22.

## Measuring before the node is in the tree
- Symptom: `global_transform` returns identity, with
  `ERROR: Condition "!is_inside_tree()" is true`; a camera framed from that lands
  at the origin.
- Cause: measuring a subtree before it is added to the scene tree.
- Fix: measure in `_ready()` or later. Treat a zero-size or identity measurement
  as a failure with a fallback, not as a small object.
- Last confirmed: 2026-08-13.

## SurfaceTool normals
- Symptom: hard edges render soft and puffy ("pillowed").
- Cause: `index()` welds vertices before `generate_normals()`, so normals average
  across corners.
- Fix: call `generate_normals()` before `index()`, or keep corners unwelded.
- Last confirmed: 2026-08-13.

## Flat geometry that never draws
- Symptom: meshes are built and counted but invisible; measurements of their
  effect never change when you scale them.
- Cause: inside-out winding on a ground-flat quad; back-face culled.
- Fix: check winding; if a metric holds steady while its subject scales, suspect
  the subject is not being drawn.
- Last confirmed: 2026-08-15.

## SpotLight3D angle
- Symptom: a spotlight lights almost nothing.
- Cause: `spot_angle` is in degrees in Godot 4; passing `deg_to_rad(46)` gives a
  0.8 degree cone.
- Fix: pass degrees.
- Last confirmed: 2026-08-15.

## Shadows that extra light cannot remove
- Symptom: a dark seam survives several added fill lights.
- Cause: it is a cast shadow from a mesh that casts by default.
- Fix: find the caster; disable its shadow casting or accept the shadow.
- Last confirmed: 2026-08-13.

## Autoloads and save files
- Symptom: a real user save changed after "just a syntax check".
- Cause: an autoload loads and migrates the default save on every boot,
  including import passes and parse checks.
- Fix: pass the scratch-slot argument (after `--`) on every run while a save
  format change is in flight; bump the save version constant last.
- Last confirmed: 2026-08-13.

## Output paths
- Symptom: a capture run reports success and writes zero images; the log shows
  a path like `res://C:\...`.
- Cause: the project's capture script treats the output path as
  `res://`-relative.
- Fix: pass a project-relative path (`--outdir=verify_out/<name>`), and check
  that the first file exists.
- Last confirmed: 2026-07 (project-specific; check your capture script).
