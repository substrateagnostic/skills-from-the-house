"""CI gate: holding the button for CHARGE_SECONDS must fire the charge.
Usage: python gate.py [--fixed-fps 60]
Without --fixed-fps the loop free-runs at the machine's speed (simulated below)."""
import sys
from game import ChargeButton, CHARGE_SECONDS

fixed = "--fixed-fps" in sys.argv
fps = 60 if fixed else 144          # CI runners free-run near the display rate
dt = 1.0 / fps

btn = ChargeButton()
hold_frames = int(CHARGE_SECONDS * 60)   # hold for 0.7s
for _ in range(hold_frames):
    btn.update(dt, True)
btn.update(dt, False)

print(f"fps={fps} frames_held={hold_frames}")
print("VERDICT: PASS" if btn.fired else "VERDICT: FAIL (charge did not fire)")
