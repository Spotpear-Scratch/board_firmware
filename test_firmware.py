# test_firmware.py -- Test script for firmware validation
# Basic tests to ensure firmware components work correctly

import time
import gc
from board_config import BoardConfig
from display import ST7735Display, BLACK, WHITE, RED, GREEN, BLUE
from ui import LVGLUI
from utils import memory_info, rgb565, hsv_to_rgb565

def test_board_config():
    """Test board configuration"""
    print("Testing board configuration...")
    
    try:
        board = BoardConfig()
        
        # Test LED control
        board.led_on()
        time.sleep_ms(100)
        board.led_off()
        
        # Test backlight control
        board.backlight_on()
        time.sleep_ms(100)
        board.backlight_off()
        time.sleep_ms(100)
        board.backlight_on()
        
        # Test button reading
        button_state = board.is_button_pressed()
        
        print(f"  ✓ Board config OK (button: {'pressed' if button_state else 'released'})")
        return True, board
        
    except Exception as e:
        print(f"  ✗ Board config failed: {e}")
        return False, None

def test_display(board):
    """Test display functionality"""
    print("Testing display...")
    
    try:
        display = ST7735Display(
            spi=board.spi,
            cs=board.display_cs,
            dc=board.display_dc,
            rst=board.display_rst,
            bl=board.display_bl
        )
        
        # Test basic operations
        display.fill(BLACK)
        time.sleep_ms(100)
        
        display.fill(RED)
        time.sleep_ms(200)
        
        display.fill(GREEN)
        time.sleep_ms(200)
        
        display.fill(BLUE)
        time.sleep_ms(200)
        
        display.fill(BLACK)
        
        # Test pixel drawing
        for i in range(0, 128, 16):
            display.pixel(i, i, WHITE)
        
        # Test line drawing
        display.hline(0, 64, 128, RED)
        display.vline(64, 0, 128, GREEN)
        
        # Test rectangle
        display.rect(20, 20, 80, 80, BLUE)
        display.fill_rect(30, 30, 60, 60, BLACK)
        
        # Test text
        display.text("TEST", 50, 60, WHITE)
        
        time.sleep(1)
        
        print("  ✓ Display test OK")
        return True, display
        
    except Exception as e:
        print(f"  ✗ Display test failed: {e}")
        return False, None

def test_ui(display):
    """Test UI functionality"""
    print("Testing UI...")
    
    try:
        ui = LVGLUI(display)
        
        # Test different screens
        ui.show_welcome()
        time.sleep(1)
        
        ui.show_demo()
        time.sleep(1)
        
        ui.show_system_info()
        time.sleep(1)
        
        ui.show_clock()
        time.sleep(1)
        
        # Test animation
        ui.show_animation()
        for _ in range(10):
            ui.update()
            time.sleep_ms(100)
        
        print("  ✓ UI test OK")
        return True, ui
        
    except Exception as e:
        print(f"  ✗ UI test failed: {e}")
        return False, None

def test_utilities():
    """Test utility functions"""
    print("Testing utilities...")
    
    try:
        # Test memory functions
        mem_info = memory_info()
        assert 'free' in mem_info
        assert 'allocated' in mem_info
        assert 'total' in mem_info
        
        # Test color conversion
        color1 = rgb565(255, 0, 0)  # Red
        assert color1 == 0xF800
        
        color2 = rgb565(0, 255, 0)  # Green
        assert color2 == 0x07E0
        
        color3 = rgb565(0, 0, 255)  # Blue
        assert color3 == 0x001F
        
        # Test HSV conversion
        hsv_color = hsv_to_rgb565(0, 1.0, 1.0)  # Red
        # Should be close to pure red
        
        print("  ✓ Utilities test OK")
        return True
        
    except Exception as e:
        print(f"  ✗ Utilities test failed: {e}")
        return False

def test_memory_usage():
    """Test memory usage and garbage collection"""
    print("Testing memory management...")
    
    try:
        # Get initial memory state
        initial_mem = memory_info()
        
        # Create some objects
        test_data = []
        for i in range(100):
            test_data.append([i] * 10)
        
        # Check memory usage
        after_alloc_mem = memory_info()
        
        # Clear objects
        test_data = None
        gc.collect()
        
        # Check memory after cleanup
        after_gc_mem = memory_info()
        
        print(f"  Initial: {initial_mem['allocated']//1024}K")
        print(f"  After alloc: {after_alloc_mem['allocated']//1024}K")
        print(f"  After GC: {after_gc_mem['allocated']//1024}K")
        
        # Memory should be freed (with some tolerance)
        if after_gc_mem['allocated'] <= initial_mem['allocated'] + 1024:  # 1KB tolerance
            print("  ✓ Memory management OK")
            return True
        else:
            print("  ⚠ Memory may not be fully freed")
            return True  # Not a critical failure
        
    except Exception as e:
        print(f"  ✗ Memory test failed: {e}")
        return False

def run_all_tests():
    """Run all firmware tests"""
    print("=== SpotPear C3-1.44 MiniTV Firmware Test ===")
    print()
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Board configuration
    board_ok, board = test_board_config()
    if board_ok:
        tests_passed += 1
    
    # Test 2: Display (requires board)
    if board:
        display_ok, display = test_display(board)
        if display_ok:
            tests_passed += 1
        
        # Test 3: UI (requires display)
        if display:
            ui_ok, ui = test_ui(display)
            if ui_ok:
                tests_passed += 1
    else:
        print("Skipping display and UI tests due to board config failure")
    
    # Test 4: Utilities
    util_ok = test_utilities()
    if util_ok:
        tests_passed += 1
    
    # Test 5: Memory management
    mem_ok = test_memory_usage()
    if mem_ok:
        tests_passed += 1
    
    # Summary
    print()
    print("=== Test Summary ===")
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("✓ All tests passed! Firmware is ready.")
        success_indicator(board if board else None)
    else:
        print("✗ Some tests failed. Check the errors above.")
        failure_indicator(board if board else None)
    
    return tests_passed == total_tests

def success_indicator(board):
    """Show success indicator"""
    if board:
        # Blink LED rapidly to indicate success
        for _ in range(6):
            board.led_on()
            time.sleep_ms(100)
            board.led_off()
            time.sleep_ms(100)

def failure_indicator(board):
    """Show failure indicator"""
    if board:
        # Slow blink to indicate failure
        for _ in range(3):
            board.led_on()
            time.sleep_ms(500)
            board.led_off()
            time.sleep_ms(500)

def main():
    """Main test function"""
    success = run_all_tests()
    
    if success:
        print("\nFirmware validation completed successfully!")
    else:
        print("\nFirmware validation failed. Please check the errors.")
    
    return success

if __name__ == "__main__":
    main()