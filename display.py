# display.py -- ST7735 TFT Display Driver for 128x128 resolution
# Optimized for SpotPear C3-1.44 MiniTV board

import time
import ustruct
from micropython import const

# ST7735 Commands
_NOP = const(0x00)
_SWRESET = const(0x01)
_RDDID = const(0x04)
_RDDST = const(0x09)
_SLPIN = const(0x10)
_SLPOUT = const(0x11)
_PTLON = const(0x12)
_NORON = const(0x13)
_INVOFF = const(0x20)
_INVON = const(0x21)
_DISPOFF = const(0x28)
_DISPON = const(0x29)
_CASET = const(0x2A)
_RASET = const(0x2B)
_RAMWR = const(0x2C)
_RAMRD = const(0x2E)
_PTLAR = const(0x30)
_COLMOD = const(0x3A)
_MADCTL = const(0x36)
_FRMCTR1 = const(0xB1)
_FRMCTR2 = const(0xB2)
_FRMCTR3 = const(0xB3)
_INVCTR = const(0xB4)
_DISSET5 = const(0xB6)
_PWCTR1 = const(0xC0)
_PWCTR2 = const(0xC1)
_PWCTR3 = const(0xC2)
_PWCTR4 = const(0xC3)
_PWCTR5 = const(0xC4)
_VMCTR1 = const(0xC5)
_RDID1 = const(0xDA)
_RDID2 = const(0xDB)
_RDID3 = const(0xDC)
_RDID4 = const(0xDD)
_PWCTR6 = const(0xFC)
_GMCTRP1 = const(0xE0)
_GMCTRN1 = const(0xE1)

# Color definitions (RGB565)
BLACK = const(0x0000)
BLUE = const(0x001F)
RED = const(0xF800)
GREEN = const(0x07E0)
CYAN = const(0x07FF)
MAGENTA = const(0xF81F)
YELLOW = const(0xFFE0)
WHITE = const(0xFFFF)

class ST7735Display:
    """ST7735 TFT Display Driver for 128x128 resolution"""
    
    def __init__(self, spi, cs, dc, rst, bl, width=128, height=128):
        """Initialize ST7735 display
        
        Args:
            spi: SPI interface
            cs: Chip select pin
            dc: Data/command pin
            rst: Reset pin
            bl: Backlight pin
            width: Display width (default 128)
            height: Display height (default 128)
        """
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.bl = bl
        self.width = width
        self.height = height
        
        # Buffer for pixel data
        self.buffer = bytearray(width * height * 2)  # RGB565 = 2 bytes per pixel
        
        # Initialize display
        self._init_display()
    
    def _write_cmd(self, cmd):
        """Write command to display"""
        self.cs.off()
        self.dc.off()  # Command mode
        self.spi.write(bytearray([cmd]))
        self.cs.on()
    
    def _write_data(self, data):
        """Write data to display"""
        self.cs.off()
        self.dc.on()  # Data mode
        if isinstance(data, int):
            self.spi.write(bytearray([data]))
        else:
            self.spi.write(data)
        self.cs.on()
    
    def _init_display(self):
        """Initialize ST7735 display"""
        print("Initializing ST7735 display...")
        
        # Hardware reset
        self.rst.off()
        time.sleep_ms(10)
        self.rst.on()
        time.sleep_ms(10)
        
        # Software reset
        self._write_cmd(_SWRESET)
        time.sleep_ms(150)
        
        # Sleep out
        self._write_cmd(_SLPOUT)
        time.sleep_ms(255)
        
        # Frame rate control
        self._write_cmd(_FRMCTR1)
        self._write_data(0x01)
        self._write_data(0x2C)
        self._write_data(0x2D)
        
        self._write_cmd(_FRMCTR2)
        self._write_data(0x01)
        self._write_data(0x2C)
        self._write_data(0x2D)
        
        self._write_cmd(_FRMCTR3)
        self._write_data(0x01)
        self._write_data(0x2C)
        self._write_data(0x2D)
        self._write_data(0x01)
        self._write_data(0x2C)
        self._write_data(0x2D)
        
        # Column inversion
        self._write_cmd(_INVCTR)
        self._write_data(0x07)
        
        # Power control
        self._write_cmd(_PWCTR1)
        self._write_data(0xA2)
        self._write_data(0x02)
        self._write_data(0x84)
        
        self._write_cmd(_PWCTR2)
        self._write_data(0xC5)
        
        self._write_cmd(_PWCTR3)
        self._write_data(0x0A)
        self._write_data(0x00)
        
        self._write_cmd(_PWCTR4)
        self._write_data(0x8A)
        self._write_data(0x2A)
        
        self._write_cmd(_PWCTR5)
        self._write_data(0x8A)
        self._write_data(0xEE)
        
        # VCOM control
        self._write_cmd(_VMCTR1)
        self._write_data(0x0E)
        
        # Display inversion off
        self._write_cmd(_INVOFF)
        
        # Memory access control
        self._write_cmd(_MADCTL)
        self._write_data(0xC8)  # RGB, row/col exchange, row reverse
        
        # Color mode: 16-bit
        self._write_cmd(_COLMOD)
        self._write_data(0x05)
        
        # Gamma correction
        self._write_cmd(_GMCTRP1)
        self._write_data(bytearray([
            0x02, 0x1c, 0x07, 0x12, 0x37, 0x32, 0x29, 0x2d,
            0x29, 0x25, 0x2B, 0x39, 0x00, 0x01, 0x03, 0x10
        ]))
        
        self._write_cmd(_GMCTRN1)
        self._write_data(bytearray([
            0x03, 0x1d, 0x07, 0x06, 0x2E, 0x2C, 0x29, 0x2D,
            0x2E, 0x2E, 0x37, 0x3F, 0x00, 0x00, 0x02, 0x10
        ]))
        
        # Normal display mode
        self._write_cmd(_NORON)
        time.sleep_ms(10)
        
        # Display on
        self._write_cmd(_DISPON)
        time.sleep_ms(100)
        
        # Turn on backlight
        self.bl.on()
        
        print("ST7735 display initialized successfully")
    
    def _set_window(self, x0, y0, x1, y1):
        """Set display window for writing pixels"""
        # Column address set
        self._write_cmd(_CASET)
        self._write_data(x0 >> 8)
        self._write_data(x0 & 0xFF)
        self._write_data(x1 >> 8)
        self._write_data(x1 & 0xFF)
        
        # Row address set
        self._write_cmd(_RASET)
        self._write_data(y0 >> 8)
        self._write_data(y0 & 0xFF)
        self._write_data(y1 >> 8)
        self._write_data(y1 & 0xFF)
        
        # Memory write
        self._write_cmd(_RAMWR)
    
    def fill(self, color):
        """Fill entire display with color"""
        color_bytes = ustruct.pack('>H', color)
        data = color_bytes * (self.width * self.height)
        
        self._set_window(0, 0, self.width - 1, self.height - 1)
        self._write_data(data)
    
    def pixel(self, x, y, color):
        """Set pixel at (x, y) to color"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self._set_window(x, y, x, y)
            self._write_data(ustruct.pack('>H', color))
    
    def hline(self, x, y, w, color):
        """Draw horizontal line"""
        if y < 0 or y >= self.height:
            return
        if x < 0:
            w += x
            x = 0
        if x + w > self.width:
            w = self.width - x
        if w <= 0:
            return
        
        color_bytes = ustruct.pack('>H', color)
        data = color_bytes * w
        self._set_window(x, y, x + w - 1, y)
        self._write_data(data)
    
    def vline(self, x, y, h, color):
        """Draw vertical line"""
        if x < 0 or x >= self.width:
            return
        if y < 0:
            h += y
            y = 0
        if y + h > self.height:
            h = self.height - y
        if h <= 0:
            return
        
        for i in range(h):
            self.pixel(x, y + i, color)
    
    def rect(self, x, y, w, h, color):
        """Draw rectangle outline"""
        self.hline(x, y, w, color)
        self.hline(x, y + h - 1, w, color)
        self.vline(x, y, h, color)
        self.vline(x + w - 1, y, h, color)
    
    def fill_rect(self, x, y, w, h, color):
        """Fill rectangle with color"""
        if x < 0:
            w += x
            x = 0
        if y < 0:
            h += y
            y = 0
        if x + w > self.width:
            w = self.width - x
        if y + h > self.height:
            h = self.height - y
        if w <= 0 or h <= 0:
            return
        
        color_bytes = ustruct.pack('>H', color)
        for row in range(h):
            data = color_bytes * w
            self._set_window(x, y + row, x + w - 1, y + row)
            self._write_data(data)
    
    def text(self, text, x, y, color=WHITE, bg_color=BLACK):
        """Simple text rendering (8x8 font)"""
        # This is a basic implementation - in practice you'd use a proper font
        for i, char in enumerate(text):
            char_x = x + i * 8
            if char_x >= self.width:
                break
            # For now, just draw a simple rectangle for each character
            self.fill_rect(char_x, y, 6, 8, color)
    
    def cleanup(self):
        """Cleanup display resources"""
        self.bl.off()  # Turn off backlight
        self._write_cmd(_DISPOFF)  # Turn off display