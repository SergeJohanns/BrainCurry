#!/usr/bin/env python3
import re
file = input("file: ")
with open(file, 'r') as script:
    with open("Minimised/min_" + file, 'w') as outscript:
        outscript.write("".join(re.findall(
            r"[<>\+\-,\.\[\]\\\|/]", script.read()
        )))