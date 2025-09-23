# SpotPear Board Firmware

For now this will only support the LV+MicroPython repo with extended support for the Spotpear C3 with the TFT driver included.

The top makefile will obtain all the necessary files, combine the board port, then compile and flash the firmware.

# Get everything, and compile, and flash the code
make all

# Rebuilt if youre making changes
make rebuild