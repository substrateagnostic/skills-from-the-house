# Pressure test: prompt-deepener

Type: output shape (the brief it writes).
Cost: one agent, no files, under 3 minutes. The agent writes a brief; it does not
dispatch it.

## Prompt (verbatim)
> Write the brief I'll hand a subagent tonight. The task: "make the night sky in
> our game look right." It's a moonlit garden party game, stylized, runs on a
> laptop GPU. The subagent has about 4 hours. Just give me the brief text.

## Failure signature (baseline)
Two or more of these:
- Opens with a persona ("You are an expert technical artist...").
- Asks for adjectives ("beautiful", "realistic", "atmospheric") without naming
  a method or measurement.
- No raw material named (no reference photos, star catalog, moon phase data,
  captured frames of the current sky, perf baseline).
- No check other than the subagent's own judgment ("make sure it looks good").
- No early checkpoint or fallback.

## Pass signature (with skill)
- Names fields and methods: e.g. real star positions or magnitude ranges, moon
  phase/brightness, sky color gradients from reference photography, a GPU frame
  cost measurement.
- Names raw material to start from: reference photos, a star catalog, current
  screenshots, the perf baseline.
- Names an outside check with a pass line: a frame-time budget measured, a
  before/after pair judged by someone who has not seen the work, or a
  readability check of silhouettes against the sky.
- Includes a kill gate (e.g. by hour 1 show a prototype at budget, else fall back
  to a painted skybox) written before work starts.

## How to score
Count the four pass elements (methods, raw material, outside check, kill gate).
Pass = all four; baseline fail = two or more failure items.
