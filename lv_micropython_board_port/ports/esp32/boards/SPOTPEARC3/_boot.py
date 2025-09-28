import gc
import vfs
from flashbdev import bdev


try:
    if bdev:
        vfs.mount(bdev, "/")
except OSError:
    import inisetup

    inisetup.setup()

gc.collect()

import time
import os
import machine

# Gets button state of the two buttons
def boot_get_button( button_number ):
    from machine import Pin
    button1 = Pin(8, Pin.IN, Pin.PULL_UP)
    button2 = Pin(10, Pin.IN, Pin.PULL_UP)

    # Since we are using pullups we need to invert the value
    if button_number == 1:
        return 1 - button1.value()
    elif button_number == 2:
        return 1 - button2.value()
    else:
        return 0

# Safety startup for main.py removal
# NOTE: Printing here seems to end up turning up in the input buffer!

#print("Short 3s delay in the event your blocks code freezes the board!\n")
#print("Press both buttons to clear the scratch code from this device...\n")
for i in range(300):  # 300 x 10ms = 2.0 seconds
    if boot_get_button(1) and boot_get_button(2):
        #print("Both buttons pressed - clearing scratch code and rebooting!\n")
        try:
            os.remove('main.py')
        except OSError:
            pass
        break
    #if i % 25 == 0:
    #    print(f"{i * 10}ms elapsed\n")
    time.sleep_ms(10)
