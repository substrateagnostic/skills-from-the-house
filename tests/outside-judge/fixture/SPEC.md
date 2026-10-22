# TALLY file format, v1

A TALLY file stores player scores for one match.

## Layout
1. Magic: the 4 bytes `TLY1`.
2. Player count: one unsigned integer, 2 bytes.
3. For each player:
   - Name length: 1 byte.
   - Name: UTF-8 bytes.
   - Score: signed integer, 4 bytes.
4. Checksum: 2 bytes, the sum of all preceding bytes.

## Example
Two players, "Al" with 10 and "Bea" with -3, encode to a 23-byte file.
