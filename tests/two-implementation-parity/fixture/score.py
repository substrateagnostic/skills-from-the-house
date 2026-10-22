def round_score(hits, misses, streak):
    """Score for one round of the party game. Used by the server; the
    browser client must show exactly the same number."""
    base = hits * 10 - misses * 7
    bonus = (streak - 3) // 2 * 5          # streak 0..10, can be negative
    penalty = misses % 3                   # every miss pattern costs a little
    raw = base + bonus - penalty
    return round(raw / 4)                  # quarter-points, rounded

if __name__ == "__main__":
    import sys
    h, m, s = map(int, sys.argv[1:4])
    print(round_score(h, m, s))
