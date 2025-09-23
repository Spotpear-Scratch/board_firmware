# example_basic_graphics.py -- Basic graphics example
# Simple demonstration of drawing primitives

import time
from board_config import BoardConfig
from display import ST7735Display, BLACK, WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA

def main():
    """Basic graphics example"""
    print("Starting basic graphics example...")
    
    # Initialize hardware
    board = BoardConfig()
    display = ST7735Display(
        spi=board.spi,
        cs=board.display_cs,
        dc=board.display_dc,
        rst=board.display_rst,
        bl=board.display_bl
    )
    
    # Clear screen
    display.fill(BLACK)
    
    # Draw some pixels
    print("Drawing pixels...")
    for x in range(0, 128, 8):
        for y in range(0, 128, 8):
            color = RED if (x + y) % 16 == 0 else WHITE
            display.pixel(x, y, color)
    
    time.sleep(2)
    
    # Draw lines
    print("Drawing lines...")
    display.fill(BLACK)
    
    # Horizontal lines
    for y in range(0, 128, 16):
        display.hline(0, y, 128, GREEN)
    
    # Vertical lines
    for x in range(0, 128, 16):
        display.vline(x, 0, 128, BLUE)
    
    time.sleep(2)
    
    # Draw rectangles
    print("Drawing rectangles...")
    display.fill(BLACK)
    
    colors = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]
    for i, color in enumerate(colors):
        x = 10 + i * 15
        y = 10 + i * 15
        w = 30
        h = 20
        display.rect(x, y, w, h, color)
    
    time.sleep(2)
    
    # Draw filled rectangles
    print("Drawing filled rectangles...")
    display.fill(BLACK)
    
    for i, color in enumerate(colors):
        x = 20 + i * 10
        y = 20 + i * 10
        w = 40 - i * 5
        h = 30 - i * 3
        display.fill_rect(x, y, w, h, color)
    
    time.sleep(2)
    
    # Simple text
    print("Drawing text...")
    display.fill(BLACK)
    display.text("Hello MiniTV!", 10, 50, WHITE)
    
    time.sleep(2)
    
    print("Basic graphics example complete!")

if __name__ == "__main__":
    main()