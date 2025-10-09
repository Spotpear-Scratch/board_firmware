name = "spotpear"

# Global imports for most spotpear blocks
# System/General imports
import os
import time
import utime

# HW Specific imports
import micropython
import machine

import random
import math

# Graphics imports
import lvgl as lv
import st77xx

##############################################################################
##############################################################################
#
# System initialization
#

def board_setup():
    # Soft reset causes a crash, so force a hard reset
    if machine.reset_cause() == machine.SOFT_RESET:
        machine.reset()     
    init_display()
    clear_screen(0x0000ff)
    button_setup_event_handler()
    set_led(0)


##############################################################################
##############################################################################
#
# Timer/sleep related functions
#

# Timers in use for various tasks
timer1 = machine.Timer(-1)
timer2 = machine.Timer(-1)
timer3 = machine.Timer(-1)
timer4 = machine.Timer(-1)
timer5 = machine.Timer(-1)

# Expects gloabal timers 1..5
def set_timer( timer = 1, _period = 5000, callback_fn = None):
    # Create a one-shot timer that triggers after 5000 milliseconds (5 seconds)
    if timer == 1:
        timer1.init(mode=machine.Timer.ONE_SHOT, period=_period, callback=callback_fn)
    elif timer == 2:
        timer2.init(mode=machine.Timer.ONE_SHOT, period=_period, callback=callback_fn)
    elif timer == 3:
        timer3.init(mode=machine.Timer.ONE_SHOT, period=_period, callback=callback_fn)
    elif timer == 4:
        timer4.init(mode=machine.Timer.ONE_SHOT, period=_period, callback=callback_fn)
    elif timer == 5:
        timer5.init(mode=machine.Timer.ONE_SHOT, period=_period, callback=callback_fn)

def sleep( ms ):
    time.sleep_ms( ms )


##############################################################################
##############################################################################
#
# Display related functions
#
def init_display():
    spi = machine.SPI( 1, baudrate=40_000_000, polarity=0, phase=0, sck=machine.Pin(3, machine.Pin.OUT), mosi=machine.Pin(4, machine.Pin.OUT), )
    disp = st77xx.St7735(rot=st77xx.ST77XX_MIRROR_PORTRAIT,res=(128,128), model='redtab', spi=spi, cs=2, dc=0, rst=5, rp2_dma=None, )
    scr = lv.obj()
    lv.screen_load(scr)
    clear_screen(0x0000ff)

def rbg_to_rgb( hexcolor ):
    """Convert 0xRBG to 0xRGB color format."""
    r = (hexcolor & 0xFF0000) >> 16
    b = (hexcolor & 0x00FF00) >> 8
    g = (hexcolor & 0x0000FF)
    return (r << 16) | (g << 8) | b


def clear_screen( color=0x003a57 ):
    screen = lv.screen_active()
    screen.clean()
    set_screen_background_color( color )

def set_screen_background_color( color ) :
    screen = lv.screen_active()
    screen.set_style_bg_color(lv.color_hex(rbg_to_rgb(color)), lv.PART.MAIN)

# Drawing a pixel at a given position with a given color
def draw_pixel( x=0, y=0, _color=0xff0000 ):
    scr = lv.screen_active()
    pixel = lv.obj(scr)
    pixel.set_size(1, 1)
    pixel.remove_flag(lv.obj.FLAG.SCROLLABLE)
    pixel.set_pos(x, y)
    pixel.set_style_bg_color(lv.color_hex(rbg_to_rgb(_color)), 0)
    return pixel

# Drawing a rectangle at a given position with a given width, height and color
def draw_rectangle(x=10, y=10, width=20, height=20, _color=0x00ff00):
    scr = lv.screen_active()
    color = lv.color_hex(rbg_to_rgb(_color))
    rect = lv.obj(scr)
    rect.set_size(width, height)
    rect.set_pos(x, y)
    rect.set_style_bg_color(color, 0)
    rect.remove_flag(lv.obj.FLAG.SCROLLABLE)
    rect.set_style_radius(0,lv.PART.MAIN)
    return rect

# Drwing a line between two points with a given color and width
def draw_line(x1=10, y1=10, x2=50, y2=50, _color=0x0000ff, width=2):
    scr = lv.screen_active()
    color = lv.color_hex(rbg_to_rgb(_color))
    line = lv.line(scr)
    line.set_points([lv.point_precise_t({"x": x1, "y": y1}), lv.point_precise_t({"x": x2, "y": y2})],2)
    line.set_style_line_color(color, 0)
    line.set_style_line_width(width, 0)
    return line

# Draws a circle at a given position with a given radius and color
def draw_circle(x=10, y=10, radius=10, _color=0xff0000):
    scr = lv.screen_active()
    color = lv.color_hex(rbg_to_rgb(_color))
    circle = lv.obj(scr)
    circle.set_size(radius * 2, radius * 2)
    circle.set_pos(x - radius, y - radius)
    circle.set_style_bg_color(color, 0)
    circle.set_style_radius(lv.RADIUS_CIRCLE, 0)
    return circle


# Draws text at a given position with a given color and size
def display_text_at_position(label_text="Hello World!", x=10, y=10, color=0xffffff, size=14):
    screen = lv.screen_active()
    label = lv.label(screen)
    lv.label.set_text(label, label_text)
    label.set_pos(x, y)
    label_style = lv.style_t()
    label_style.init()
    if size == 14:
        font = lv.font_montserrat_14
    elif size == 16:
        font = lv.font_montserrat_16
    elif size == 24:
        font = lv.font_montserrat_24
    else:
        font = lv.font_montserrat_14  # Default to 14 if size is unrecognized
    label_style.set_text_font(font)
    label_style.set_text_color(lv.color_hex(rbg_to_rgb(color)))
    label.add_style(label_style, 0)
    return label

# For matrix displaying we need to parse the string into a 2D array 
def parse_matrix(input_str):
    """
    Converts a colon-separated string of digits into an NxN matrix of integers.
    
    Example:
        '09090:90909:90009:09090:00900' → 
        [[0,9,0,9,0],
         [9,0,9,0,9],
         [9,0,0,0,9],
         [0,9,0,9,0],
         [0,0,9,0,0]]
    """
    rows = input_str.split(':')
    matrix = [[int(char) for char in row] for row in rows]
    
    # Optional: Validate it's a square matrix
    n = len(matrix)
    if not all(len(row) == n for row in matrix):
        raise ValueError("Input does not form a square NxN matrix.")
    
    return matrix

# DRaws a NxN grid based on a 2D array of 0s and 1s
def draw_grid(grid, border, square_color, screen_width, screen_height):
    N = len(grid)
    if N == 0 or any(len(row) != N for row in grid):
        raise ValueError("Grid must be NxN")
    # Calculate available space and square size
    total_border_x = border * (N + 1)
    total_border_y = border * (N + 1)
    square_width = (screen_width - total_border_x) // N
    square_height = (screen_height - total_border_y) // N
    # Get the current screen
    screen = lv.screen_active()
    # Draw each square
    for row in range(N):
        for col in range(N):
            if grid[row][col] == 1:
                x = border + col * (square_width + border)
                y = border + row * (square_height + border)
                #
                square = lv.obj(screen)
                square.set_size(square_width, square_height)
                square.set_pos(x, y)
                square.remove_flag(lv.obj.FLAG.SCROLLABLE)
                square.set_style_radius(0,lv.PART.MAIN)
                #
                square.set_style_bg_color(lv.color_hex(rbg_to_rgb(square_color)), lv.PART.MAIN)
                # We just dont draw anything if its missing
                #else:
                #    square.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
                #
                square.set_style_border_width(1, lv.PART.MAIN)
                square.set_style_border_color(lv.color_hex(0x000000), lv.PART.MAIN)


##############################################################################
##############################################################################
#
# LED/PIN Handlers
#

# Sets the LED to on of off
def set_led( boolean ):
    from machine import Pin
    led = Pin(11, Pin.OUT)
    if boolean == 0:
        led.off()
    else:
        led.on()

# Sets a pin high or low
def set_pin( pin_number, boolean ):
    from machine import Pin
    if pin_number == 1:
        pin = Pin(1, Pin.OUT)
    elif pin_number == 2:
        pin = Pin(6, Pin.OUT)
    elif pin_number == 3:
        pin = Pin(21, Pin.OUT)
    elif pin_number == 4:
        pin = Pin(20, Pin.OUT)

    if boolean == 1:
        pin.off()
    else:
        pin.on( )



##############################################################################
##############################################################################
#
# Button related functions
#

_button1_user_callback = None
_button2_user_callback = None
_button_both_user_callback = None

last_button_ms = -1
_spbutton1_pressed = False
_spbutton2_pressed = False


# No longer direct read
def get_button( button_number ): 
    global _spbutton1_pressed, _spbutton2_pressed
    tval = None
    if button_number == 1:
        tval = _spbutton1_pressed
        _spbutton1_pressed = False
    elif button_number == 2:
        tval = _spbutton2_pressed
        _spbutton2_pressed = False
    return tval


# Allow setting of callbacks from main user program
# NOTE: Any number other than 1 or 2 means 
#       both buttons 1 and 2 are pressed within a period of time
#
def set_button_callback(button_number, _callback):
    global _button1_user_callback, _button2_user_callback, _button_both_user_callback
    if button_number == 1:
        _button1_user_callback = _callback
    elif button_number == 2:
        _button2_user_callback = _callback
    else:  # Both buttons
        _button_both_user_callback = _callback

# This is called from the IRQ via schedule
def safe_button_handler(pin):
    global last_button_ms, _spbutton1_pressed, _spbutton2_pressed, _button1_user_callback, _button2_user_callback, _button_both_user_callback, _spbutton1, _spbutton2
    # Determine which button
    otherbutton_pressed = False
    button = 0
    if pin == _spbutton1:
        print("Button1 : Interrupt triggered!")
        otherbutton_pressed = _spbutton2_pressed
        button = 1
    elif pin == _spbutton2:
        print("Button2 : Interrupt triggered!")
        otherbutton_pressed = _spbutton1_pressed
        button = 2
    #
    # Get current time
    current_ms = utime.ticks_ms()
    # Handle first time button press
    if last_button_ms == -1:
        last_button_ms = current_ms + 9999  # Just a large number to avoid immediate trigger
    #
    # Check if both buttons pressed within 200ms
    delta_ms = utime.ticks_diff(current_ms, last_button_ms)
    if delta_ms < 200 and otherbutton_pressed:
        last_button_ms = current_ms
        #
        # If callback is defined, then do it
        if _button_both_user_callback is not None:
            _spbutton1_pressed = False
            _spbutton2_pressed = False
            _button_both_user_callback()
            return
    # Update last button time
    last_button_ms = current_ms
    #
    #
    if button == 1:
        print("Button1 : Pressed!")
        # Event block callback for button 1
        if _button1_user_callback is not None:
            print("Button1 : Pressed - trying a callback!")
            _spbutton1_pressed = False
            _button1_user_callback()
            return
        #
        # For manual button reads
        _spbutton1_pressed = True
        return
    #
    if button == 2:
        # Event block callback for button 2
        if _button2_user_callback is not None:
            _spbutton2_pressed = False
            _button2_user_callback()
            return
        #
        # For manual button reads
        _spbutton2_pressed = True
        return



# ISR cant allocate memory so we use schedule to call a function later
def button1_handler(pin):
    micropython.schedule(safe_button_handler, pin)

def button2_handler(pin):
    micropython.schedule(safe_button_handler, pin)

def button_setup_event_handler():
    from machine import Pin
    global _spbutton1_pressed, _spbutton2_pressed, _spbutton1, _spbutton2
    #
    # Setup buttons with IRQs
    _spbutton1_pressed = False
    _spbutton1 = Pin(8, Pin.IN)
    _spbutton1.irq(trigger=Pin.IRQ_RISING, handler=button1_handler)
    #
    _spbutton2_pressed = False
    _spbutton2 = Pin(10, Pin.IN)
    _spbutton2.irq(trigger=Pin.IRQ_RISING, handler=button2_handler)



##############################################################################
##############################################################################
#
# Helper functions for vfs operations
#

# Remove a file if it exists
def fs_rm( filename="main.py" ):
    try:
        os.remove(filename)
    except OSError:
        pass

# Create a file from stdin
def fs_write( filename="main.py" ):
    print("Enter your input line by line. Press Ctrl+D (or Ctrl+Z on Windows) to finish:")
    try:
        with open(filename, "w") as f:
            while True:
                try:
                    line = input()
                    f.write(line + "\n")
                except EOFError:
                    break
        print("All lines written to ", filename)
    except Exception as e:
        print(f"An error occurred: {e}")

# List files in the current directory with sizes and modification dates
def fs_ls():
    try:
        files = os.listdir()
        for file in files:
            if os.stat(file)[0] & 0x8000:  # Check if it's a regular file
                stat = os.stat(file)
                size = stat[6]
                # Some MicroPython ports support mtime in stat[8]
                try:
                    mtime = stat[8]
                    print(f"{file} — {size} bytes — Last modified: {mtime}")
                except IndexError:
                    print(f"{file} — {size} bytes")
        print("End of file list.")
    except Exception as e:
        print("Error:", e)

# Dump a text file to stdout
def fs_cat(filename):
    try:
        with open(filename, 'r') as f:
            for line in f:
                print(line, end='')  # Avoid double newlines
    except Exception as e:
        print("Error reading file:", e)

