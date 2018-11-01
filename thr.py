import threading
from threading import Timer
import time

def printit():
  threading.Timer(5.0, printit).start()
  print (time.time())

printit()