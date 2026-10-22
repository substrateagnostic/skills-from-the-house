# Overnight run - Edition 2, 23:58

## Needs you
nothing needed

## Done since last edition
- Fog shader ported (shots/fog_before.png, shots/fog_after.png); gate PASS (logs/gate_2.log).

## Findings
- Draw calls down from 412 to 380 (measured, logs/perf_2.log).

## Not shown / not checked
- Fog not checked on the projector profile.

## In flight
- Shadow cascade rework, expected ~01:00.

## What I got wrong
- 23:20 (Edition 1 said the menu crash was fixed. It was not: it repro'd at 23:40 on a cold start. Re-opened.)
