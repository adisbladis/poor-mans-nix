#!/usr/bin/env python
import haxxpkgs
import sys


if __name__ == "__main__":
    drv = getattr(haxxpkgs, sys.argv[1])
    print(str(drv()))
