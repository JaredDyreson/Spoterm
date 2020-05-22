#!/usr/bin/env python3.8

try:
  while(True):
    instruction = input(">>> ")
    print("\t\t\t{}".format(instruction))
except (EOFError, KeyboardInterrupt) as error:
    print("exiting!")
