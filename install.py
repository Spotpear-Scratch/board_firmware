# install.py -- Installation script for SpotPear C3-1.44 MiniTV firmware
# Helps users install the firmware on their boards

import os
import sys

def check_micropython():
    """Check if running on MicroPython"""
    try:
        import machine
        import micropython
        return True
    except ImportError:
        return False

def check_required_modules():
    """Check if all required modules are available"""
    required_modules = [
        'machine',
        'time', 
        'gc',
        'ustruct',
        'utime',
        'random',
        'math'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    return missing_modules

def test_hardware():
    """Test basic hardware functionality"""
    if not check_micropython():
        print("Error: This script must run on MicroPython")
        return False
    
    try:
        import machine
        
        # Test SPI
        spi = machine.SPI(1, baudrate=1000000, sck=machine.Pin(2), mosi=machine.Pin(3))
        print("✓ SPI interface available")
        
        # Test GPIO pins
        test_pins = [6, 7, 8, 9, 10, 11]
        for pin_num in test_pins:
            pin = machine.Pin(pin_num, machine.Pin.OUT)
            pin.on()
            pin.off()
        print("✓ GPIO pins functional")
        
        return True
        
    except Exception as e:
        print(f"✗ Hardware test failed: {e}")
        return False

def install_firmware():
    """Install firmware files"""
    print("SpotPear C3-1.44 MiniTV Firmware Installation")
    print("=" * 50)
    
    # Check environment
    if check_micropython():
        print("✓ Running on MicroPython")
    else:
        print("✗ This firmware requires MicroPython")
        print("Please install MicroPython on your ESP32-C3 board first")
        return False
    
    # Check required modules
    missing = check_required_modules()
    if missing:
        print(f"✗ Missing required modules: {', '.join(missing)}")
        print("Please ensure you have a complete MicroPython installation")
        return False
    else:
        print("✓ All required modules available")
    
    # Test hardware
    if test_hardware():
        print("✓ Hardware test passed")
    else:
        print("✗ Hardware test failed")
        print("Please check your board connections")
        return False
    
    # Check if firmware files exist
    required_files = [
        'boot.py',
        'main.py', 
        'board_config.py',
        'display.py',
        'ui.py',
        'demos.py',
        'utils.py',
        'config.py'
    ]
    
    missing_files = []
    for filename in required_files:
        if not os.path.exists(filename):
            missing_files.append(filename)
    
    if missing_files:
        print(f"✗ Missing firmware files: {', '.join(missing_files)}")
        print("Please ensure all firmware files are uploaded to the board")
        return False
    else:
        print("✓ All firmware files present")
    
    # Run basic functionality test
    try:
        print("Testing firmware components...")
        
        # Test board config
        from board_config import BoardConfig
        board = BoardConfig()
        print("✓ Board configuration OK")
        
        # Test display initialization (without full init to avoid conflicts)
        from display import ST7735Display
        print("✓ Display driver OK")
        
        # Test UI components
        from ui import LVGLUI
        print("✓ UI components OK")
        
        # Test utilities
        from utils import memory_info
        mem_info = memory_info()
        print(f"✓ Utilities OK (Memory: {mem_info['allocated']//1024}K/{mem_info['total']//1024}K)")
        
    except Exception as e:
        print(f"✗ Firmware test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✓ Firmware installation successful!")
    print("\nNext steps:")
    print("1. Reset your board or run: import main; main.main()")
    print("2. Press the boot button to switch between modes")
    print("3. Check examples/ directory for sample applications")
    print("4. Read README.md for detailed documentation")
    
    return True

def show_usage():
    """Show usage information"""
    print("SpotPear C3-1.44 MiniTV Firmware")
    print("Usage:")
    print("  import install; install.install_firmware()  - Run installation")
    print("  import install; install.test_hardware()     - Test hardware only")
    print("  import main; main.main()                     - Start main application")
    print("")
    print("Files in this firmware:")
    print("  boot.py          - Boot configuration")
    print("  main.py          - Main application")
    print("  board_config.py  - Hardware configuration")
    print("  display.py       - ST7735 display driver")
    print("  ui.py            - User interface layer")
    print("  demos.py         - Demo applications")
    print("  utils.py         - Utility functions")
    print("  config.py        - Advanced configuration")
    print("  test_firmware.py - Firmware validation tests")
    print("  examples/        - Example applications")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_usage()
    else:
        install_firmware()