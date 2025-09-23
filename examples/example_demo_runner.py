# example_demo_runner.py -- Comprehensive demo runner
# Runs all available demos with menu system

import time
from board_config import BoardConfig
from display import ST7735Display, BLACK, WHITE, GREEN, CYAN, YELLOW
from demos import DemoApps
from utils import ButtonHandler, print_system_info

class DemoRunner:
    """Comprehensive demo runner with menu system"""
    
    def __init__(self):
        """Initialize demo runner"""
        self.board = BoardConfig()
        self.display = ST7735Display(
            spi=self.board.spi,
            cs=self.board.display_cs,
            dc=self.board.display_dc,
            rst=self.board.display_rst,
            bl=self.board.display_bl
        )
        self.demos = DemoApps(self.display, self.board)
        
        # Menu system
        self.menu_items = [
            ("Color Test", self.demos.run_color_test),
            ("Pixel Test", self.demos.run_pixel_test),
            ("Line Test", self.demos.run_line_test),
            ("Rectangle Test", self.demos.run_rect_test),
            ("Spiral Demo", self.demos.run_spiral_demo),
            ("Animation Demo", self.demos.run_animation_demo),
            ("Sine Wave Demo", self.demos.run_sine_wave_demo),
            ("Text Demo", self.demos.run_text_demo),
            ("All Demos", self.demos.run_all_demos),
            ("System Info", self.show_system_info),
        ]
        
        self.current_menu_index = 0
        self.in_menu = True
        self.button = ButtonHandler(self.board.btn_boot, self.on_button_press)
        
    def on_button_press(self):
        """Handle button press"""
        if self.in_menu:
            # Navigate menu
            self.current_menu_index = (self.current_menu_index + 1) % len(self.menu_items)
            self.show_menu()
        else:
            # Run selected demo
            self.run_current_demo()
    
    def show_menu(self):
        """Show menu screen"""
        self.display.fill(BLACK)
        
        # Title
        self._draw_centered_text("Demo Menu", 10, CYAN)
        
        # Menu items
        start_y = 30
        for i, (name, _) in enumerate(self.menu_items):
            y = start_y + i * 12
            if y > 120:  # Don't draw off screen
                break
                
            color = YELLOW if i == self.current_menu_index else WHITE
            prefix = "> " if i == self.current_menu_index else "  "
            
            self._draw_text(prefix + name, 5, y, color)
        
        # Instructions
        self._draw_centered_text("Press to select", 115, GREEN)
    
    def run_current_demo(self):
        """Run the currently selected demo"""
        if 0 <= self.current_menu_index < len(self.menu_items):
            name, demo_func = self.menu_items[self.current_menu_index]
            
            self.display.fill(BLACK)
            self._draw_centered_text(f"Running {name}", 50, GREEN)
            self._draw_centered_text("Press to continue", 70, WHITE)
            time.sleep(2)
            
            try:
                demo_func()
            except Exception as e:
                print(f"Demo error: {e}")
                self.display.fill(BLACK)
                self._draw_centered_text("Demo Error", 50, YELLOW)
                self._draw_centered_text(str(e)[:20], 70, WHITE)
                time.sleep(3)
            
            # Return to menu
            self.show_menu()
    
    def show_system_info(self):
        """Show system information on display"""
        from utils import get_system_info
        
        self.display.fill(BLACK)
        info = get_system_info()
        
        # Draw system info
        self._draw_text("System Info", 5, 5, CYAN)
        self._draw_text(f"Platform: {info['platform']}", 5, 20, WHITE)
        self._draw_text(f"CPU: {info['freq']//1000000}MHz", 5, 35, WHITE)
        
        mem = info['memory']
        self._draw_text(f"Memory:", 5, 50, WHITE)
        self._draw_text(f"{mem['allocated']//1024}K/{mem['total']//1024}K", 5, 65, GREEN)
        
        self._draw_text(f"Usage: {mem['usage_percent']:.1f}%", 5, 80, WHITE)
        self._draw_text(f"ID: {info['unique_id'][:8]}...", 5, 95, WHITE)
        
        time.sleep(5)
        self.show_menu()
    
    def _draw_text(self, text, x, y, color):
        """Draw text at position"""
        self.display.text(text, x, y, color)
    
    def _draw_centered_text(self, text, y, color):
        """Draw centered text"""
        text_width = len(text) * 8
        x = (self.display.width - text_width) // 2
        self._draw_text(text, x, y, color)
    
    def run(self):
        """Run the demo runner"""
        print("Starting Demo Runner...")
        print_system_info()
        
        # Show initial menu
        self.show_menu()
        
        try:
            while True:
                # Update button state
                self.button.update()
                
                # Small delay
                time.sleep_ms(50)
                
        except KeyboardInterrupt:
            print("Demo runner stopped by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        self.display.fill(BLACK)
        self.display.cleanup()
        self.board.led_off()

def main():
    """Main function"""
    runner = DemoRunner()
    runner.run()

if __name__ == "__main__":
    main()