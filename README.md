# SpotPear C3-1.44 MiniTV Board Firmware

Firmware for the SpotPear C3-1.44 inch MiniTV board with ST7735 128x128 TFT display using MicroPython with additional LVGL graphics widget layer.

## Features

- **MicroPython-based**: Easy to program and modify
- **ST7735 TFT Display Driver**: Full support for 128x128 resolution display
- **LVGL Graphics Layer**: High-level UI widgets and graphics
- **Hardware Abstraction**: Clean board configuration and pin mapping
- **Demo Applications**: Various example programs showcasing capabilities
- **Utility Functions**: Helper functions for common tasks

## Hardware Specifications

- **MCU**: ESP32-C3 (RISC-V single-core, 160MHz)
- **Display**: ST7735 128x128 TFT LCD
- **Interface**: SPI
- **Memory**: 400KB SRAM, 4MB Flash
- **GPIO**: Multiple available for expansion

## Pin Configuration

| Function | GPIO Pin | Description |
|----------|----------|-------------|
| SPI SCK  | GPIO2    | SPI Clock |
| SPI MOSI | GPIO3    | SPI Data |
| Display CS | GPIO7  | Chip Select |
| Display DC | GPIO6  | Data/Command |
| Display RST | GPIO10 | Reset |
| Display BL | GPIO11 | Backlight |
| Button | GPIO9 | Boot/User Button |
| LED | GPIO8 | Built-in LED |

## File Structure

```
board_firmware/
├── boot.py              # Boot configuration
├── main.py              # Main application entry point
├── board_config.py      # Board-specific pin configuration
├── display.py           # ST7735 display driver
├── ui.py                # LVGL UI wrapper and widgets
├── demos.py             # Demo applications
├── utils.py             # Utility functions
├── examples/            # Example applications
└── README.md           # This file
```

## Quick Start

1. **Flash MicroPython**: Install MicroPython on your ESP32-C3 board
2. **Upload Files**: Copy all `.py` files to the board
3. **Run**: The firmware will start automatically on boot

## Basic Usage

### Display Text
```python
from board_config import BoardConfig
from display import ST7735Display

board = BoardConfig()
display = ST7735Display(board.spi, board.display_cs, board.display_dc, 
                       board.display_rst, board.display_bl)

display.fill(0x0000)  # Clear screen (black)
display.text("Hello World!", 10, 50, 0xFFFF)  # White text
```

### Use UI System
```python
from board_config import BoardConfig
from display import ST7735Display
from ui import LVGLUI

board = BoardConfig()
display = ST7735Display(board.spi, board.display_cs, board.display_dc,
                       board.display_rst, board.display_bl)
ui = LVGLUI(display)

ui.show_welcome()
```

### Run Demos
```python
from board_config import BoardConfig
from display import ST7735Display
from demos import DemoApps

board = BoardConfig()
display = ST7735Display(board.spi, board.display_cs, board.display_dc,
                       board.display_rst, board.display_bl)
demos = DemoApps(display, board)

demos.run_all_demos()
```

## API Reference

### BoardConfig Class
```python
board = BoardConfig()
board.backlight_on()     # Turn on display backlight
board.backlight_off()    # Turn off display backlight
board.led_on()           # Turn on built-in LED
board.led_off()          # Turn off built-in LED
board.is_button_pressed() # Check if button is pressed
```

### ST7735Display Class
```python
display = ST7735Display(spi, cs, dc, rst, bl)
display.fill(color)                    # Fill screen with color
display.pixel(x, y, color)             # Set pixel
display.hline(x, y, width, color)      # Horizontal line
display.vline(x, y, height, color)     # Vertical line
display.rect(x, y, w, h, color)        # Rectangle outline
display.fill_rect(x, y, w, h, color)   # Filled rectangle
display.text(text, x, y, color)        # Simple text
```

### LVGLUI Class
```python
ui = LVGLUI(display)
ui.show_welcome()        # Welcome screen
ui.show_demo()           # Graphics demo
ui.show_clock()          # Clock display
ui.show_system_info()    # System information
ui.show_animation()      # Animation demo
ui.next_screen()         # Switch to next screen
ui.update()              # Update animations (call in loop)
```

## Color Constants

The firmware includes predefined colors in RGB565 format:
- `BLACK` (0x0000)
- `WHITE` (0xFFFF)
- `RED` (0xF800)
- `GREEN` (0x07E0)
- `BLUE` (0x001F)
- `YELLOW` (0xFFE0)
- `CYAN` (0x07FF)
- `MAGENTA` (0xF81F)

## Utilities

### Memory Management
```python
from utils import memory_info, print_memory_info, force_gc

print_memory_info()  # Print current memory usage
force_gc()           # Force garbage collection
```

### Color Conversion
```python
from utils import rgb565, hsv_to_rgb565

color = rgb565(255, 128, 0)        # RGB to RGB565
color = hsv_to_rgb565(120, 1.0, 1.0)  # HSV to RGB565
```

### Animation Helpers
```python
from utils import Interpolator, AnimationEasing

# Animate value from 0 to 100 over 1 second
interp = Interpolator(0, 100, 1000, AnimationEasing.ease_out_quad)
current_value = interp.get_value()
```

## Examples

See the `examples/` directory for complete example applications:
- Simple graphics demos
- Interactive applications
- Animation examples
- Custom UI widgets

## Development

### Adding New Features
1. Follow the existing code structure
2. Use the hardware abstraction layer
3. Add utility functions to `utils.py`
4. Create demos in `demos.py`

### Performance Tips
- Use `gc.collect()` regularly for long-running applications
- Buffer pixel operations when possible
- Use appropriate delays for animations
- Monitor memory usage with utility functions

## Troubleshooting

### Display Issues
- Check SPI connections
- Verify pin assignments in `board_config.py`
- Ensure proper power supply
- Test with simple fill/pixel operations

### Memory Issues
- Use `force_gc()` to check memory usage
- Optimize large data structures
- Break down complex operations

### Performance Issues
- Reduce animation frame rates
- Use simpler graphics operations
- Profile code with timing utilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following the existing code style
4. Test on actual hardware
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check the troubleshooting section
- Review example code
- Open an issue on GitHub