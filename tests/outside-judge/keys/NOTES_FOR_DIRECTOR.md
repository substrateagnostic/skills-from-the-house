Planted ambiguities in SPEC.md (do NOT give this file to the test agent):
1. Byte order never stated (reference is big-endian).
2. Name length: is it bytes or characters? (reference: UTF-8 byte count)
3. Checksum overflow: "sum of all preceding bytes" in 2 bytes; truncation/mod 65536 unstated.
4. Checksum byte order (big-endian) unstated.
5. Name length limit (255) and behavior for longer names unstated.
6. Example gives a length (23) but no hex bytes, so it cannot settle 1, 3, 4.
A reader with tally.py open answers all of these from code and tends not to notice them.
