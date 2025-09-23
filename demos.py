# demos.py -- Demo applications for SpotPear C3-1.44 MiniTV
# Various demonstration programs showcasing display capabilities

import time
import random
import math
from display import BLACK, WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA

class DemoApps:
    """Collection of demo applications"""
    
    def __init__(self, display, board):
        """Initialize demo applications
        
        Args:
            display: ST7735Display instance
            board: BoardConfig instance
        """
        self.display = display
        self.board = board
        self.width = display.width
        self.height = display.height
    
    def run_color_test(self):
        """Test all colors"""
        print("Running color test...")
        
        colors = [BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE]
        color_names = ["BLACK", "RED", "GREEN", "BLUE", "YELLOW", "CYAN", "MAGENTA", "WHITE"]
        
        for i, (color, name) in enumerate(zip(colors, color_names)):
            self.display.fill(color)
            print(f"Displaying {name}")
            time.sleep(1)
            
            # Blink LED to indicate progress
            self.board.led_on()
            time.sleep(0.1)
            self.board.led_off()
    
    def run_pixel_test(self):
        """Test individual pixel drawing"""
        print("Running pixel test...")
        
        self.display.fill(BLACK)
        
        # Draw random pixels
        for _ in range(1000):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            color = random.choice([RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE])
            self.display.pixel(x, y, color)
            
            if random.randint(0, 100) == 0:  # Occasional delay
                time.sleep_ms(10)
    
    def run_line_test(self):
        """Test line drawing"""
        print("Running line test...")
        
        self.display.fill(BLACK)
        
        # Horizontal lines
        for y in range(0, self.height, 8):
            color = [RED, GREEN, BLUE, YELLOW][y // 32]
            self.display.hline(0, y, self.width, color)
            time.sleep_ms(50)
        
        time.sleep(1)
        
        # Vertical lines
        self.display.fill(BLACK)
        for x in range(0, self.width, 8):
            color = [CYAN, MAGENTA, WHITE, YELLOW][x // 32]
            self.display.vline(x, 0, self.height, color)
            time.sleep_ms(50)
    
    def run_rect_test(self):
        """Test rectangle drawing"""
        print("Running rectangle test...")
        
        self.display.fill(BLACK)
        
        # Nested rectangles
        colors = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]
        for i, color in enumerate(colors):
            size = 10 + i * 15
            x = (self.width - size) // 2
            y = (self.height - size) // 2
            self.display.rect(x, y, size, size, color)
            time.sleep_ms(200)
        
        time.sleep(1)
        
        # Filled rectangles
        self.display.fill(BLACK)
        for i in range(8):
            x = i * 15
            y = i * 10
            w = 20
            h = 15
            color = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE, RED][i]
            self.display.fill_rect(x, y, w, h, color)
            time.sleep_ms(200)
    
    def run_animation_demo(self):
        """Run animation demonstration"""
        print("Running animation demo...")
        
        # Bouncing ball animation
        ball_x = 20
        ball_y = 20
        vel_x = 2
        vel_y = 3
        radius = 8
        
        for frame in range(200):  # Run for ~10 seconds at 20fps
            # Clear screen
            self.display.fill(BLACK)
            
            # Update ball position
            ball_x += vel_x
            ball_y += vel_y
            
            # Bounce off walls
            if ball_x - radius <= 0 or ball_x + radius >= self.width:
                vel_x = -vel_x
                ball_x = max(radius, min(self.width - radius, ball_x))
            
            if ball_y - radius <= 0 or ball_y + radius >= self.height:
                vel_y = -vel_y
                ball_y = max(radius, min(self.height - radius, ball_y))
            
            # Draw ball
            self._draw_filled_circle(ball_x, ball_y, radius, RED)
            
            # Draw trail
            for i in range(3):
                trail_x = ball_x - vel_x * (i + 1)
                trail_y = ball_y - vel_y * (i + 1)
                trail_radius = radius - i - 1
                if trail_radius > 0:
                    color = [YELLOW, GREEN, BLUE][i]
                    self._draw_filled_circle(trail_x, trail_y, trail_radius, color)
            
            # Draw borders
            self.display.rect(0, 0, self.width, self.height, WHITE)
            
            time.sleep_ms(50)  # 20 FPS
            
            # Check for button press to exit
            if self.board.is_button_pressed():
                break
    
    def run_spiral_demo(self):
        """Draw a colorful spiral"""
        print("Running spiral demo...")
        
        self.display.fill(BLACK)
        
        center_x = self.width // 2
        center_y = self.height // 2
        max_radius = min(center_x, center_y) - 5
        
        for i in range(0, 360 * 3, 2):  # 3 full rotations
            angle = math.radians(i)
            radius = (i / (360 * 3)) * max_radius
            
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))
            
            # Color changes based on angle
            color_index = (i // 60) % 6
            color = [RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA][color_index]
            
            if 0 <= x < self.width and 0 <= y < self.height:
                self.display.pixel(x, y, color)
            
            if i % 20 == 0:  # Update every 20 degrees
                time.sleep_ms(10)
    
    def run_sine_wave_demo(self):
        """Draw animated sine waves"""
        print("Running sine wave demo...")
        
        for frame in range(100):
            self.display.fill(BLACK)
            
            # Draw multiple sine waves with different frequencies and phases
            for wave in range(3):
                frequency = 0.05 + wave * 0.02
                phase = frame * 0.1 + wave * math.pi / 3
                amplitude = 20 + wave * 10
                center_y = self.height // 2
                color = [RED, GREEN, BLUE][wave]
                
                for x in range(self.width):
                    y = center_y + int(amplitude * math.sin(frequency * x + phase))
                    if 0 <= y < self.height:
                        self.display.pixel(x, y, color)
            
            time.sleep_ms(50)
            
            # Check for button press to exit
            if self.board.is_button_pressed():
                break
    
    def run_text_demo(self):
        """Demonstrate text rendering"""
        print("Running text demo...")
        
        messages = [
            ("Hello", RED),
            ("SpotPear", GREEN),
            ("MiniTV", BLUE),
            ("ST7735", YELLOW),
            ("128x128", CYAN),
            ("Display", MAGENTA),
        ]
        
        for i, (text, color) in enumerate(messages):
            self.display.fill(BLACK)
            
            # Center the text
            text_width = len(text) * 8
            x = (self.width - text_width) // 2
            y = self.height // 2 - 4
            
            # Draw background box
            self.display.fill_rect(x - 4, y - 4, text_width + 8, 16, WHITE)
            
            # Draw text (using display's text method)
            self.display.text(text, x, y, color, WHITE)
            
            time.sleep(1)
    
    def _draw_filled_circle(self, cx, cy, radius, color):
        """Helper method to draw a filled circle"""
        for y in range(-radius, radius + 1):
            for x in range(-radius, radius + 1):
                if x * x + y * y <= radius * radius:
                    px = cx + x
                    py = cy + y
                    if 0 <= px < self.width and 0 <= py < self.height:
                        self.display.pixel(px, py, color)
    
    def run_all_demos(self):
        """Run all demos in sequence"""
        print("Starting demo sequence...")
        
        demos = [
            self.run_color_test,
            self.run_pixel_test,
            self.run_line_test,
            self.run_rect_test,
            self.run_spiral_demo,
            self.run_animation_demo,
            self.run_sine_wave_demo,
            self.run_text_demo,
        ]
        
        for demo in demos:
            try:
                demo()
                time.sleep(1)  # Pause between demos
            except KeyboardInterrupt:
                print("Demo interrupted by user")
                break
            except Exception as e:
                print(f"Demo error: {e}")
                continue
        
        print("Demo sequence complete")