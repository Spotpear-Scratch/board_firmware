# boot.py -- run on boot-up
# This file is executed on every boot (including wake-boot from deepsleep)

import gc
import machine
import network
import utime

# Basic setup
gc.collect()

# Configure WiFi in STA mode (disabled by default)
sta_if = network.WLAN(network.STA_IF)
sta_if.active(False)

# Configure AP mode (disabled by default)
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

print("SpotPear C3-1.44 MiniTV Board Boot Complete")
print("Memory info:", gc.mem_alloc(), "/", gc.mem_alloc() + gc.mem_free())