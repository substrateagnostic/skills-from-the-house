import struct

def encode(players):
    """players: list of (name, score). Reference implementation."""
    body = b"TLY1" + struct.pack(">H", len(players))
    for name, score in players:
        raw = name.encode("utf-8")
        body += struct.pack(">B", len(raw)) + raw + struct.pack(">i", score)
    checksum = sum(body) & 0xFFFF
    return body + struct.pack(">H", checksum)

def decode(data):
    assert data[:4] == b"TLY1"
    n = struct.unpack(">H", data[4:6])[0]
    i, out = 6, []
    for _ in range(n):
        ln = data[i]; i += 1
        name = data[i:i+ln].decode("utf-8"); i += ln
        score = struct.unpack(">i", data[i:i+4])[0]; i += 4
        out.append((name, score))
    assert sum(data[:i]) & 0xFFFF == struct.unpack(">H", data[i:i+2])[0]
    return out

if __name__ == "__main__":
    b = encode([("Al", 10), ("Bea", -3)])
    print(len(b), b.hex())
