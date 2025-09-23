# example_animated_clock.py -- Animated digital clock
# Shows current time with smooth animations

import time
import math
from board_config import BoardConfig
from display import ST7735Display, BLACK, WHITE, RED, GREEN, BLUE, CYAN
from utils import Interpolator, AnimationEasing, hsv_to_rgb565

class AnimatedClock:
    """Animated digital clock application"""
    
    def __init__(self):
        """Initialize animated clock"""
        self.board = BoardConfig()
        self.display = ST7735Display(
            spi=self.board.spi,
            cs=self.board.display_cs,
            dc=self.board.display_dc,
            rst=self.board.display_rst,
            bl=self.board.display_bl
        )
        
        # Animation state
        self.last_second = -1
        self.color_hue = 0
        self.pulse_animator = Interpolator(0, 1, 1000, AnimationEasing.ease_in_out_quad)
        
    def draw_time(self, hours, minutes, seconds):
        """Draw time with animations"""
        # Create time string
        time_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        
        # Calculate position (centered)
        text_width = len(time_str) * 8
        x = (self.display.width - text_width) // 2
        y = self.display.height // 2 - 4
        
        # Get pulse value for animation
        pulse = self.pulse_animator.get_value()
        if self.pulse_animator.is_complete():
            self.pulse_animator.reset()
        
        # Calculate animated color based on pulse and hue
        brightness = 0.7 + 0.3 * pulse
        color = hsv_to_rgb565(self.color_hue, 1.0, brightness)
        
        # Draw background with pulse effect
        bg_size = int(10 + 5 * pulse)
        bg_x = x - bg_size
        bg_y = y - bg_size
        bg_w = text_width + 2 * bg_size
        bg_h = 16 + 2 * bg_size
        
        # Ensure background doesn't go off screen
        bg_x = max(0, bg_x)
        bg_y = max(0, bg_y)
        bg_w = min(bg_w, self.display.width - bg_x)
        bg_h = min(bg_h, self.display.height - bg_y)
        
        self.display.fill_rect(bg_x, bg_y, bg_w, bg_h, BLACK)
        
        # Draw time
        self._draw_text_with_shadow(time_str, x, y, color)
        
        # Draw seconds indicator
        self._draw_seconds_arc(seconds)
        
        # Draw corner decorations
        self._draw_corner_decorations()
        
    def _draw_text_with_shadow(self, text, x, y, color):
        """Draw text with shadow effect"""
        # Draw shadow
        self.display.text(text, x + 1, y + 1, BLACK)
        # Draw main text
        self.display.text(text, x, y, color)
    
    def _draw_seconds_arc(self, seconds):
        """Draw arc showing seconds progress"""
        center_x = self.display.width // 2
        center_y = self.display.height // 2
        radius = 50
        
        # Calculate arc length based on seconds
        arc_angle = (seconds / 60.0) * 360
        
        # Draw arc as series of pixels
        for angle in range(0, int(arc_angle), 2):
            rad = math.radians(angle - 90)  # Start from top
            x = center_x + int(radius * math.cos(rad))
            y = center_y + int(radius * math.sin(rad))
            
            if 0 <= x < self.display.width and 0 <= y < self.display.height:
                # Color changes based on progress
                hue = (angle / 360.0) * 360
                color = hsv_to_rgb565(hue, 1.0, 0.8)
                self.display.pixel(x, y, color)
    
    def _draw_corner_decorations(self):
        """Draw decorative elements in corners"""
        corners = [
            (5, 5),           # Top-left
            (118, 5),         # Top-right
            (5, 118),         # Bottom-left
            (118, 118)        # Bottom-right
        ]
        
        for i, (cx, cy) in enumerate(corners):
            # Animated color for each corner
            hue = (self.color_hue + i * 90) % 360
            color = hsv_to_rgb565(hue, 1.0, 0.6)
            
            # Draw small animated square
            size = 3 + int(2 * abs(math.sin(time.ticks_ms() / 1000.0 + i)))
            self.display.fill_rect(cx - size//2, cy - size//2, size, size, color)
    
    def run(self):
        """Run the animated clock"""
        print("Starting animated clock...")
        print("Press Ctrl+C to exit")
        
        try:
            while True:
                # Get current time
                current_time = time.localtime()
                hours = current_time[3]
                minutes = current_time[4] 
                seconds = current_time[5]
                
                # Check if second changed for animation trigger
                if seconds != self.last_second:
                    self.last_second = seconds
                    # Reset pulse animation on second change
                    self.pulse_animator.reset()
                    
                    # Slowly cycle through colors
                    self.color_hue = (self.color_hue + 6) % 360
                    
                    # Blink LED on second change
                    self.board.led_on()
                    time.sleep_ms(50)
                    self.board.led_off()
                
                # Clear screen
                self.display.fill(BLACK)
                
                # Draw animated time
                self.draw_time(hours, minutes, seconds)
                
                # Update at 20 FPS
                time.sleep_ms(50)
                
        except KeyboardInterrupt:
            print("Clock stopped by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        self.display.fill(BLACK)
        self.display.cleanup()
        self.board.led_off()

def main():
    """Main function"""
    clock = AnimatedClock()
    clock.run()

if __name__ == "__main__":
    main()