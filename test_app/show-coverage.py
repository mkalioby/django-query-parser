#!/usr/bin/env python3
import subprocess
x=subprocess.run(["coverage", "report"],stdout=subprocess.PIPE)
print("Coverage:", x.stdout.decode("utf8").split("\n")[-2].split()[-1])
