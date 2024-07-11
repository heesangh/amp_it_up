

import time
import os
import math
import random

from terminalio import FONT
from adafruit_display_text import label, wrap_text_to_lines
import adafruit_bitmapsaver
import adafruit_imageload

excluded_libs = ["code.py", "main.py", "hardware.py", "menu.py"]
active_app = "menu.py"
working_directory = os.getcwd()
base_directory = os.getcwd()
dir_hist = []

print("\n -- hardware loading -- ")
with open("hardware.py", "r") as file:
    exec(file.read(), globals())
print(" -- hardware loaded -- \n")

#print("\n -- brickbreaker loading -- ")
#with open("brickbreaker.py", "r") as file:
#    exec(file.read(), globals())
#print(" -- brickbreaker loaded -- \n")


print(" -- menu entered -- ")
with open("menu.py", "r") as file:
    exec(file.read(), globals())
print(" -- menu exited -- \n")

while True:
    if(active_app[-4:] == ".txt"):
        os.chdir(base_directory)
        print(" -- text reading: ", active_app)
        with open("textreader.py", 'r') as file:
            exec(file.read(), globals())
        print(" -- text exiting -- ")
    elif(active_app[-4:] == ".bmp"):
        os.chdir(base_directory)
        print(" -- bmp reading: ", active_app)
        with open("bmpreader.py", 'r') as file:
            exec(file.read(), globals())
        print(" -- bmp exiting -- ")
    elif(active_app[-3:] == ".py"):
        print("loading: ", active_app)
        with open(active_app, "r") as file:
            exec(file.read(), globals())
        print("exiting: ", active_app)

    os.chdir(base_directory)
    print(" -- menu entered -- ")
    with open("menu.py", "r") as file:
        exec(file.read(), globals())
    print(" -- menu exited -- ")



#print("----- pico   code -----")
#for f in os.listdir():
#    if(f[-3:] == ".py" and f not in excluded_libs):
#        print(f[:-3], " loading")
#        with open(f, "r") as file:
#            exec(file.read(), globals())
#            file.close()

#os.chdir("sd")
#print("----- sdcard code -----")
#for f in os.listdir():
#    if(f[-3:] == ".py" and f not in excluded_libs):
#        print(f[:-3], " loading")
#        with open(f, "r") as file:
#            exec(file.read(), globals())
#            file.close()


