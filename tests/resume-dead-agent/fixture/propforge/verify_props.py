import os, sys
want = [f"prop_{i:02d}.glb" for i in range(1, 11)]
have = set(os.listdir(os.path.join(os.path.dirname(__file__), "out")))
missing = [w for w in want if w not in have]
print("VERDICT: PASS" if not missing else f"VERDICT: FAIL missing {missing}")
