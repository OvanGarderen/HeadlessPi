#!/usr/bin/env python
# Callback test; just to see if callbacks are working.

from time import sleep
import cec

print("Loaded CEC from", cec.__file__)

class OBJ:
    def __init__(self):
        cec.add_callback(self.cb, cec.EVENT_ALL & ~cec.EVENT_LOG)
        cec.init()

    def cb(*args):
        print("Got args ")
        for arg in args:
            print(arg)
        print("\n\n\n")

        # arguments: iils
    def log_cb(self, event, level, time, message):
        print("CEC Log message:", message)

#cec.add_callback(log_cb, cec.EVENT_LOG)
object = OBJ()
sleep(1000000)

