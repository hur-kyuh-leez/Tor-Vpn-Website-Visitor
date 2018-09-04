import time
import os

while True:

    os.system('tor&')
    time.sleep(3)
    os.system('pkill tor')