import os
import sys

ret = os.fork()

if ret == 0:
    print(os.getpid(), os.getppid(), "child")
    # exit()
elif ret > 0:
    print(os.getpid(), ret, "parent")
    # exit()
sys.exit(1)
