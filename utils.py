# utils.py -- Utility functions for SpotPear C3-1.44 MiniTV
# Common utility functions and helpers

import time
import gc
import machine

def memory_info():
    """Get memory information"""
    mem_free = gc.mem_free()
    mem_alloc = gc.mem_alloc()
    mem_total = mem_free + mem_alloc
    
    return {
        'free': mem_free,
        'allocated': mem_alloc,
        'total': mem_total,
        'usage_percent': (mem_alloc / mem_total) * 100
    }

def print_memory_info():
    """Print formatted memory information"""
    info = memory_info()
    print(f"Memory: {info['allocated']//1024}K/{info['total']//1024}K ({info['usage_percent']:.1f}%)")

def force_gc():
    """Force garbage collection and print memory info"""
    print("Before GC:", end=" ")
    print_memory_info()
    gc.collect()
    print("After GC:", end=" ")
    print_memory_info()

def rgb565(r, g, b):
    """Convert RGB888 to RGB565 format
    
    Args:
        r: Red value (0-255)
        g: Green value (0-255)
        b: Blue value (0-255)
    
    Returns:
        RGB565 color value
    """
    r = (r >> 3) & 0x1F
    g = (g >> 2) & 0x3F
    b = (b >> 3) & 0x1F
    return (r << 11) | (g << 5) | b

def hsv_to_rgb565(h, s, v):
    """Convert HSV to RGB565
    
    Args:
        h: Hue (0-360)
        s: Saturation (0-1)
        v: Value (0-1)
    
    Returns:
        RGB565 color value
    """
    import math
    
    h = h % 360
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    r = int((r + m) * 255)
    g = int((g + m) * 255)
    b = int((b + m) * 255)
    
    return rgb565(r, g, b)

class Timer:
    """Simple timer utility"""
    
    def __init__(self):
        self.start_time = time.ticks_ms()
    
    def reset(self):
        """Reset timer"""
        self.start_time = time.ticks_ms()
    
    def elapsed(self):
        """Get elapsed time in milliseconds"""
        return time.ticks_diff(time.ticks_ms(), self.start_time)
    
    def elapsed_seconds(self):
        """Get elapsed time in seconds"""
        return self.elapsed() / 1000.0

class FPSCounter:
    """FPS counter utility"""
    
    def __init__(self, sample_size=10):
        self.sample_size = sample_size
        self.frame_times = []
        self.last_frame_time = time.ticks_ms()
    
    def frame(self):
        """Call this once per frame"""
        current_time = time.ticks_ms()
        frame_time = time.ticks_diff(current_time, self.last_frame_time)
        self.last_frame_time = current_time
        
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.sample_size:
            self.frame_times.pop(0)
    
    def get_fps(self):
        """Get current FPS"""
        if len(self.frame_times) < 2:
            return 0
        
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        if avg_frame_time == 0:
            return 0
        
        return 1000.0 / avg_frame_time

class ButtonHandler:
    """Button press handler with debouncing"""
    
    def __init__(self, pin, callback=None, debounce_ms=50):
        """Initialize button handler
        
        Args:
            pin: machine.Pin object
            callback: Function to call on button press
            debounce_ms: Debounce time in milliseconds
        """
        self.pin = pin
        self.callback = callback
        self.debounce_ms = debounce_ms
        self.last_press_time = 0
        self.last_state = self.pin.value()
    
    def update(self):
        """Update button state - call this regularly"""
        current_state = self.pin.value()
        current_time = time.ticks_ms()
        
        # Check for state change (button pressed = low)
        if self.last_state and not current_state:  # Falling edge
            if time.ticks_diff(current_time, self.last_press_time) > self.debounce_ms:
                self.last_press_time = current_time
                if self.callback:
                    self.callback()
                return True
        
        self.last_state = current_state
        return False

class AnimationEasing:
    """Animation easing functions"""
    
    @staticmethod
    def linear(t):
        """Linear interpolation"""
        return t
    
    @staticmethod
    def ease_in_quad(t):
        """Quadratic ease in"""
        return t * t
    
    @staticmethod
    def ease_out_quad(t):
        """Quadratic ease out"""
        return 1 - (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_out_quad(t):
        """Quadratic ease in-out"""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - 2 * (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_cubic(t):
        """Cubic ease in"""
        return t * t * t
    
    @staticmethod
    def ease_out_cubic(t):
        """Cubic ease out"""
        return 1 - (1 - t) ** 3
    
    @staticmethod
    def bounce(t):
        """Bounce effect"""
        import math
        return abs(math.sin(6.28 * t)) * (1 - t)

class Interpolator:
    """Value interpolator for animations"""
    
    def __init__(self, start_value, end_value, duration_ms, easing_func=None):
        """Initialize interpolator
        
        Args:
            start_value: Starting value
            end_value: Ending value
            duration_ms: Duration in milliseconds
            easing_func: Easing function (default: linear)
        """
        self.start_value = start_value
        self.end_value = end_value
        self.duration_ms = duration_ms
        self.easing_func = easing_func or AnimationEasing.linear
        self.start_time = time.ticks_ms()
    
    def get_value(self):
        """Get current interpolated value"""
        elapsed = time.ticks_diff(time.ticks_ms(), self.start_time)
        if elapsed >= self.duration_ms:
            return self.end_value
        
        t = elapsed / self.duration_ms
        eased_t = self.easing_func(t)
        
        return self.start_value + (self.end_value - self.start_value) * eased_t
    
    def is_complete(self):
        """Check if interpolation is complete"""
        elapsed = time.ticks_diff(time.ticks_ms(), self.start_time)
        return elapsed >= self.duration_ms
    
    def reset(self, new_start=None, new_end=None):
        """Reset interpolator with optional new values"""
        if new_start is not None:
            self.start_value = new_start
        if new_end is not None:
            self.end_value = new_end
        self.start_time = time.ticks_ms()

def clamp(value, min_val, max_val):
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))

def lerp(a, b, t):
    """Linear interpolation between a and b"""
    return a + (b - a) * t

def map_range(value, in_min, in_max, out_min, out_max):
    """Map value from one range to another"""
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def get_system_info():
    """Get system information"""
    info = {
        'platform': 'ESP32-C3',
        'firmware': 'MicroPython',
        'memory': memory_info(),
        'freq': machine.freq(),
        'unique_id': machine.unique_id().hex(),
    }
    
    return info

def print_system_info():
    """Print formatted system information"""
    info = get_system_info()
    print("=== System Information ===")
    print(f"Platform: {info['platform']}")
    print(f"Firmware: {info['firmware']}")
    print(f"CPU Freq: {info['freq']//1000000}MHz")
    print(f"Unique ID: {info['unique_id']}")
    print(f"Memory: {info['memory']['allocated']//1024}K/{info['memory']['total']//1024}K")
    print("==========================")