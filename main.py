# main.py -- Main application entry point
# SpotPear C3-1.44 MiniTV Board Main Application

import gc
import machine
import utime
from board_config import BoardConfig
from display import ST7735Display, BLACK, WHITE, GREEN, CYAN, YELLOW
from ui import LVGLUI
from utils import ButtonHandler, print_system_info

class MiniTVApp:
    """Main MiniTV application"""
    
    def __init__(self):
        """Initialize the application"""
        print("Starting SpotPear C3-1.44 MiniTV Application...")
        
        # Initialize board configuration
        self.board = BoardConfig()
        
        # Initialize display
        print("Initializing ST7735 Display...")
        self.display = ST7735Display(
            spi=self.board.spi,
            cs=self.board.display_cs,
            dc=self.board.display_dc,
            rst=self.board.display_rst,
            bl=self.board.display_bl
        )
        
        # Initialize UI
        print("Initializing UI...")
        self.ui = LVGLUI(self.display)
        
        # Button handler for mode switching
        self.button = ButtonHandler(self.board.btn_boot, self.on_button_press)
        
        # Application modes
        self.modes = [
            ("Welcome", self.ui.show_welcome),
            ("Demo", self.ui.show_demo),
            ("Clock", self.ui.show_clock),
            ("Info", self.ui.show_system_info),
            ("Animation", self.ui.show_animation),
        ]
        self.current_mode = 0
        
        # State
        self.running = True
        
        print_system_info()
        print("Application initialized. Memory:", gc.mem_alloc(), "/", gc.mem_alloc() + gc.mem_free())
    
    def on_button_press(self):
        """Handle button press to switch modes"""
        self.current_mode = (self.current_mode + 1) % len(self.modes)
        mode_name, mode_func = self.modes[self.current_mode]
        
        print(f"Switching to mode: {mode_name}")
        mode_func()
        
        # Indicate mode switch with LED
        self.board.led_on()
        utime.sleep_ms(100)
        self.board.led_off()
    
    def show_startup_screen(self):
        """Show startup screen with instructions"""
        self.display.fill(BLACK)
        
        # Draw title
        self._draw_centered_text("SpotPear", 20, CYAN)
        self._draw_centered_text("MiniTV", 35, WHITE)
        
        # Draw instructions
        self._draw_centered_text("Press button", 70, GREEN)
        self._draw_centered_text("to switch modes", 85, GREEN)
        
        # Draw border
        self.display.rect(5, 5, self.display.width - 10, self.display.height - 10, WHITE)
        
        utime.sleep(2)
    
    def _draw_centered_text(self, text, y, color):
        """Draw centered text"""
        text_width = len(text) * 8
        x = (self.display.width - text_width) // 2
        self.display.text(text, x, y, color)
    
    def run(self):
        """Run the main application"""
        # Show startup screen
        self.show_startup_screen()
        
        # Start with welcome screen
        self.ui.show_welcome()
        
        print("Application running. Press button to switch modes.")
        print("Available modes:", [name for name, _ in self.modes])
        
        try:
            while self.running:
                # Update button state
                self.button.update()
                
                # Update UI animations
                self.ui.update()
                
                # Periodic garbage collection
                if utime.ticks_ms() % 10000 < 50:  # Every ~10 seconds
                    gc.collect()
                
                # Small delay to prevent busy waiting
                utime.sleep_ms(50)
                
        except KeyboardInterrupt:
            print("Application stopped by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup application resources"""
        print("Cleaning up...")
        self.ui.cleanup()
        self.display.cleanup()
        self.board.led_off()
        print("Cleanup complete")

def main():
    """Main application entry point"""
    app = MiniTVApp()
    app.run()

if __name__ == "__main__":
    main()