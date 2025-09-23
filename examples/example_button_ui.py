# example_button_ui.py -- Interactive button-controlled UI
# Demonstrates button handling and screen switching

import time
from board_config import BoardConfig
from display import ST7735Display
from ui import LVGLUI
from utils import ButtonHandler

class ButtonUI:
    """Button-controlled UI example"""
    
    def __init__(self):
        """Initialize button UI"""
        self.board = BoardConfig()
        self.display = ST7735Display(
            spi=self.board.spi,
            cs=self.board.display_cs,
            dc=self.board.display_dc,
            rst=self.board.display_rst,
            bl=self.board.display_bl
        )
        self.ui = LVGLUI(self.display)
        
        # Button handler with callback
        self.button = ButtonHandler(self.board.btn_boot, self.on_button_press)
        
        # State
        self.running = True
        
    def on_button_press(self):
        """Handle button press"""
        print("Button pressed - switching screen")
        self.ui.next_screen()
        
        # Blink LED to indicate button press
        self.board.led_on()
        time.sleep_ms(100)
        self.board.led_off()
    
    def run(self):
        """Run the interactive UI"""
        print("Starting button-controlled UI...")
        print("Press button to switch screens")
        
        # Show initial screen
        self.ui.show_welcome()
        
        try:
            while self.running:
                # Update button state
                self.button.update()
                
                # Update UI animations
                self.ui.update()
                
                # Small delay to prevent busy waiting
                time.sleep_ms(50)
                
        except KeyboardInterrupt:
            print("UI stopped by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        self.ui.cleanup()
        self.display.cleanup()
        self.board.led_off()

def main():
    """Main function"""
    app = ButtonUI()
    app.run()

if __name__ == "__main__":
    main()