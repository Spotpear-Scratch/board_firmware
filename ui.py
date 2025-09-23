# ui.py -- LVGL UI wrapper for SpotPear C3-1.44 MiniTV
# Provides high-level UI functionality using LVGL

import time
import gc
from display import BLACK, WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA

class LVGLUI:
    """LVGL UI wrapper for the MiniTV board"""
    
    def __init__(self, display):
        """Initialize LVGL UI
        
        Args:
            display: ST7735Display instance
        """
        self.display = display
        self.width = display.width
        self.height = display.height
        
        # UI state
        self.current_screen = "welcome"
        self.animation_frame = 0
        self.last_update = time.ticks_ms()
        
        # Initialize display with black background
        self.display.fill(BLACK)
    
    def show_welcome(self):
        """Show welcome screen"""
        self.current_screen = "welcome"
        self.display.fill(BLACK)
        
        # Draw title
        self._draw_centered_text("SpotPear", 30, WHITE)
        self._draw_centered_text("MiniTV", 50, CYAN)
        
        # Draw border
        self.display.rect(2, 2, self.width - 4, self.height - 4, WHITE)
        
        # Draw version info
        self._draw_centered_text("v1.0", 90, GREEN)
        
        print("Welcome screen displayed")
    
    def show_demo(self):
        """Show graphics demo"""
        self.current_screen = "demo"
        self.display.fill(BLACK)
        
        # Draw colorful rectangles
        colors = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]
        rect_size = 20
        
        for i, color in enumerate(colors):
            x = (i % 3) * 40 + 10
            y = (i // 3) * 30 + 20
            self.display.fill_rect(x, y, rect_size, rect_size, color)
        
        # Draw title
        self._draw_centered_text("Demo", 100, WHITE)
        
        print("Demo screen displayed")
    
    def show_clock(self):
        """Show clock screen"""
        self.current_screen = "clock"
        self.display.fill(BLACK)
        
        # Get current time (simplified)
        current_time = time.localtime()
        hours = current_time[3]
        minutes = current_time[4]
        seconds = current_time[5]
        
        # Format time
        time_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        
        # Draw time
        self._draw_centered_text(time_str, 60, WHITE)
        
        # Draw clock frame
        self.display.rect(10, 40, self.width - 20, 50, CYAN)
        
        print("Clock screen displayed")
    
    def show_system_info(self):
        """Show system information"""
        self.current_screen = "info"
        self.display.fill(BLACK)
        
        # Memory info
        mem_free = gc.mem_free()
        mem_alloc = gc.mem_alloc()
        mem_total = mem_free + mem_alloc
        
        # Draw info
        self._draw_text("System Info", 10, 10, WHITE)
        self._draw_text("Memory:", 10, 30, CYAN)
        self._draw_text("{}K/{}K".format(mem_alloc//1024, mem_total//1024), 10, 45, GREEN)
        
        self._draw_text("Display:", 10, 65, CYAN)
        self._draw_text("128x128", 10, 80, GREEN)
        self._draw_text("ST7735", 10, 95, GREEN)
        
        print("System info displayed")
    
    def show_animation(self):
        """Show animation demo"""
        self.current_screen = "animation"
        
        # Clear background
        self.display.fill(BLACK)
        
        # Animate a bouncing ball
        center_x = self.width // 2
        center_y = self.height // 2
        radius = 15
        
        # Calculate position based on animation frame
        offset_x = int(30 * (self.animation_frame / 50.0))
        offset_y = int(20 * ((self.animation_frame % 100) / 100.0))
        
        if (self.animation_frame // 50) % 2:
            offset_x = 30 - offset_x
        
        ball_x = center_x + offset_x - radius
        ball_y = center_y + offset_y - radius
        
        # Draw ball
        self._draw_circle(ball_x + radius, ball_y + radius, radius, RED)
        
        # Draw trail
        for i in range(5):
            trail_alpha = 5 - i
            if trail_alpha > 0:
                trail_x = ball_x - i * 5
                trail_y = ball_y - i * 2
                self._draw_circle(trail_x + radius, trail_y + radius, radius - i, 
                                BLUE if i % 2 else GREEN)
        
        print("Animation frame:", self.animation_frame)
    
    def _draw_text(self, text, x, y, color):
        """Draw text at specified position"""
        # Simple character rendering - each char is 8x8
        for i, char in enumerate(text):
            char_x = x + i * 8
            if char_x + 8 > self.width:
                break
            self._draw_char(char, char_x, y, color)
    
    def _draw_centered_text(self, text, y, color):
        """Draw centered text"""
        text_width = len(text) * 8
        x = (self.width - text_width) // 2
        self._draw_text(text, x, y, color)
    
    def _draw_char(self, char, x, y, color):
        """Draw a single character (simplified)"""
        # This is a very basic character renderer
        # In practice, you would use a proper font bitmap
        
        # Simple pattern for basic characters
        patterns = {
            'A': [0x18, 0x3C, 0x66, 0x66, 0x7E, 0x66, 0x66, 0x00],
            'B': [0x7C, 0x66, 0x66, 0x7C, 0x66, 0x66, 0x7C, 0x00],
            'C': [0x3C, 0x66, 0x60, 0x60, 0x60, 0x66, 0x3C, 0x00],
            'D': [0x78, 0x6C, 0x66, 0x66, 0x66, 0x6C, 0x78, 0x00],
            'E': [0x7E, 0x60, 0x60, 0x78, 0x60, 0x60, 0x7E, 0x00],
            'F': [0x7E, 0x60, 0x60, 0x78, 0x60, 0x60, 0x60, 0x00],
            'G': [0x3C, 0x66, 0x60, 0x6E, 0x66, 0x66, 0x3C, 0x00],
            'H': [0x66, 0x66, 0x66, 0x7E, 0x66, 0x66, 0x66, 0x00],
            'I': [0x3C, 0x18, 0x18, 0x18, 0x18, 0x18, 0x3C, 0x00],
            'J': [0x1E, 0x0C, 0x0C, 0x0C, 0x0C, 0x6C, 0x38, 0x00],
            'K': [0x66, 0x6C, 0x78, 0x70, 0x78, 0x6C, 0x66, 0x00],
            'L': [0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x7E, 0x00],
            'M': [0x63, 0x77, 0x7F, 0x6B, 0x63, 0x63, 0x63, 0x00],
            'N': [0x66, 0x76, 0x7E, 0x7E, 0x6E, 0x66, 0x66, 0x00],
            'O': [0x3C, 0x66, 0x66, 0x66, 0x66, 0x66, 0x3C, 0x00],
            'P': [0x7C, 0x66, 0x66, 0x7C, 0x60, 0x60, 0x60, 0x00],
            'Q': [0x3C, 0x66, 0x66, 0x66, 0x66, 0x3C, 0x0E, 0x00],
            'R': [0x7C, 0x66, 0x66, 0x7C, 0x78, 0x6C, 0x66, 0x00],
            'S': [0x3C, 0x66, 0x60, 0x3C, 0x06, 0x66, 0x3C, 0x00],
            'T': [0x7E, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x00],
            'U': [0x66, 0x66, 0x66, 0x66, 0x66, 0x66, 0x3C, 0x00],
            'V': [0x66, 0x66, 0x66, 0x66, 0x66, 0x3C, 0x18, 0x00],
            'W': [0x63, 0x63, 0x63, 0x6B, 0x7F, 0x77, 0x63, 0x00],
            'X': [0x66, 0x66, 0x3C, 0x18, 0x3C, 0x66, 0x66, 0x00],
            'Y': [0x66, 0x66, 0x66, 0x3C, 0x18, 0x18, 0x18, 0x00],
            'Z': [0x7E, 0x06, 0x0C, 0x18, 0x30, 0x60, 0x7E, 0x00],
            ' ': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            ':': [0x00, 0x18, 0x18, 0x00, 0x18, 0x18, 0x00, 0x00],
            '0': [0x3C, 0x66, 0x6E, 0x76, 0x66, 0x66, 0x3C, 0x00],
            '1': [0x18, 0x18, 0x38, 0x18, 0x18, 0x18, 0x7E, 0x00],
            '2': [0x3C, 0x66, 0x06, 0x0C, 0x30, 0x60, 0x7E, 0x00],
            '3': [0x3C, 0x66, 0x06, 0x1C, 0x06, 0x66, 0x3C, 0x00],
            '4': [0x06, 0x0E, 0x1E, 0x66, 0x7F, 0x06, 0x06, 0x00],
            '5': [0x7E, 0x60, 0x7C, 0x06, 0x06, 0x66, 0x3C, 0x00],
            '6': [0x3C, 0x66, 0x60, 0x7C, 0x66, 0x66, 0x3C, 0x00],
            '7': [0x7E, 0x66, 0x0C, 0x18, 0x18, 0x18, 0x18, 0x00],
            '8': [0x3C, 0x66, 0x66, 0x3C, 0x66, 0x66, 0x3C, 0x00],
            '9': [0x3C, 0x66, 0x66, 0x3E, 0x06, 0x66, 0x3C, 0x00],
        }
        
        pattern = patterns.get(char.upper(), patterns[' '])
        
        for row in range(8):
            byte = pattern[row]
            for col in range(8):
                if byte & (0x80 >> col):
                    self.display.pixel(x + col, y + row, color)
    
    def _draw_circle(self, cx, cy, radius, color):
        """Draw a filled circle"""
        for y in range(-radius, radius + 1):
            for x in range(-radius, radius + 1):
                if x * x + y * y <= radius * radius:
                    px = cx + x
                    py = cy + y
                    if 0 <= px < self.width and 0 <= py < self.height:
                        self.display.pixel(px, py, color)
    
    def update(self):
        """Update UI - call this regularly in main loop"""
        current_time = time.ticks_ms()
        
        # Update animation frame
        if time.ticks_diff(current_time, self.last_update) >= 100:  # 10 FPS
            self.animation_frame += 1
            self.last_update = current_time
            
            # Update animation screen if active
            if self.current_screen == "animation":
                self.show_animation()
            elif self.current_screen == "clock":
                self.show_clock()
    
    def next_screen(self):
        """Switch to next screen"""
        screens = ["welcome", "demo", "clock", "info", "animation"]
        current_index = screens.index(self.current_screen)
        next_index = (current_index + 1) % len(screens)
        next_screen = screens[next_index]
        
        if next_screen == "welcome":
            self.show_welcome()
        elif next_screen == "demo":
            self.show_demo()
        elif next_screen == "clock":
            self.show_clock()
        elif next_screen == "info":
            self.show_system_info()
        elif next_screen == "animation":
            self.show_animation()
    
    def cleanup(self):
        """Cleanup UI resources"""
        self.display.fill(BLACK)
        print("UI cleaned up")