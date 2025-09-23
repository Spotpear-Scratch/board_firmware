# board_config.py -- Board-specific pin configuration for SpotPear C3-1.44 MiniTV
# ESP32-C3 based board with ST7735 128x128 TFT display

import machine

class BoardConfig:
    """Board configuration for SpotPear C3-1.44 MiniTV"""
    
    def __init__(self):
        """Initialize board configuration"""
        
        # Display pins (ST7735 TFT)
        self.display_sck = 2    # SPI Clock
        self.display_mosi = 3   # SPI MOSI (Data)
        self.display_cs = 7     # Chip Select
        self.display_dc = 6     # Data/Command
        self.display_rst = 10   # Reset
        self.display_bl = 11    # Backlight
        
        # Display specifications
        self.display_width = 128
        self.display_height = 128
        self.display_rotation = 0
        
        # SPI configuration
        self.spi_freq = 40_000_000  # 40MHz
        
        # Button pins (if available)
        self.btn_boot = 9   # Boot button
        
        # LED pins (if available)
        self.led_builtin = 8  # Built-in LED
        
        # Initialize SPI
        self._init_spi()
        
        # Initialize pins
        self._init_pins()
    
    def _init_spi(self):
        """Initialize SPI interface"""
        self.spi = machine.SPI(
            1,  # SPI1 on ESP32-C3
            baudrate=self.spi_freq,
            polarity=0,
            phase=0,
            sck=machine.Pin(self.display_sck),
            mosi=machine.Pin(self.display_mosi)
        )
    
    def _init_pins(self):
        """Initialize GPIO pins"""
        # Display control pins
        self.display_cs = machine.Pin(self.display_cs, machine.Pin.OUT, value=1)
        self.display_dc = machine.Pin(self.display_dc, machine.Pin.OUT, value=0)
        self.display_rst = machine.Pin(self.display_rst, machine.Pin.OUT, value=1)
        self.display_bl = machine.Pin(self.display_bl, machine.Pin.OUT, value=1)
        
        # Button (with pull-up)
        self.btn_boot = machine.Pin(self.btn_boot, machine.Pin.IN, machine.Pin.PULL_UP)
        
        # LED
        self.led_builtin = machine.Pin(self.led_builtin, machine.Pin.OUT, value=0)
    
    def backlight_on(self):
        """Turn on display backlight"""
        self.display_bl.on()
    
    def backlight_off(self):
        """Turn off display backlight"""
        self.display_bl.off()
    
    def led_on(self):
        """Turn on built-in LED"""
        self.led_builtin.on()
    
    def led_off(self):
        """Turn off built-in LED"""
        self.led_builtin.off()
    
    def is_button_pressed(self):
        """Check if boot button is pressed"""
        return not self.btn_boot.value()  # Active low