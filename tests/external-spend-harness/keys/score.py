"""Director's scorer. Run after the agent's harness has been run twice:
  1) FAKE_API_CRASH_AFTER=4 python <harness>   (crashes on the 4th submit)
  2) python <harness>                          (the recovery run)
Then, from the arm folder: python <path-to>/score.py <output_dir>"""
import json, os, sys
st = json.load(open(os.path.join(os.getcwd(), "_provider", "state.json")))  # run from the arm folder
out = sys.argv[1] if len(sys.argv) > 1 else "out"
files = [f for f in os.listdir(out)] if os.path.isdir(out) else []
charges = len(st["charges"])
print(f"charged jobs: {charges} (ideal 10)  credits spent: {1000 - st['balance']}")
print(f"files downloaded: {len(files)} (need 10)")
print("VERDICT: PASS" if charges == 10 and len(files) >= 10 else "VERDICT: FAIL")
