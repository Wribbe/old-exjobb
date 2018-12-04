#!/usr/bin/env python3

import sys

filename = sys.argv[1]
lines = [l.strip("\n") for l in open(filename).readlines()]

output = []
for line in lines:
    chars = []
    if line.startswith("%"):
        continue
    for char in line:
        if char in ['%']:
            if chars[-1] != "\\":
                chars.append("\\")
        chars.append(char)
    output.append(''.join(chars))

print('\n'.join(output))
