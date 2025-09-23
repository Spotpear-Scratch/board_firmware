# config.py -- Advanced configuration options
# Configuration file for advanced users to customize firmware behavior

# Display Configuration
DISPLAY_CONFIG = {
    # Display orientation (0, 1, 2, 3 for 0°, 90°, 180°, 270°)
    'rotation': 0,
    
    # Color inversion
    'invert_colors': False,
    
    # Backlight PWM control (if supported)
    'backlight_pwm': False,
    'backlight_brightness': 100,  # 0-100%
    
    # SPI frequency (Hz)
    'spi_frequency': 40_000_000,  # 40MHz
    
    # Display timing (microseconds)
    'reset_delay_us': 10000,
    'init_delay_us': 150000,
}

# UI Configuration
UI_CONFIG = {
    # Animation settings
    'animation_fps': 20,
    'animation_enabled': True,
    
    # Text settings
    'default_text_color': 0xFFFF,  # White
    'default_bg_color': 0x0000,    # Black
    
    # Screen timeouts (milliseconds)
    'screen_timeout': 30000,  # 30 seconds
    'demo_timeout': 10000,    # 10 seconds per demo
    
    # UI effects
    'fade_transitions': True,
    'bounce_animations': True,
}

# Application Configuration
APP_CONFIG = {
    # Auto-start mode
    'auto_start_mode': 'welcome',  # 'welcome', 'demo', 'clock', 'info'
    
    # Button behavior
    'button_debounce_ms': 50,
    'button_long_press_ms': 1000,
    
    # Memory management
    'auto_gc_interval': 10000,  # Auto GC every 10 seconds
    'memory_warning_threshold': 80,  # Warning at 80% memory usage
    
    # Debug settings
    'debug_mode': False,
    'verbose_logging': False,
    'show_fps': False,
}

# Hardware Configuration
HARDWARE_CONFIG = {
    # Pin mappings (can be overridden for custom boards)
    'pins': {
        'spi_sck': 2,
        'spi_mosi': 3,
        'display_cs': 7,
        'display_dc': 6,
        'display_rst': 10,
        'display_bl': 11,
        'button': 9,
        'led': 8,
    },
    
    # Power management
    'low_power_mode': False,
    'cpu_frequency': 160000000,  # 160MHz
    
    # I2C configuration (if needed for sensors)
    'i2c_enabled': False,
    'i2c_sda': 5,
    'i2c_scl': 4,
    'i2c_frequency': 100000,
}

# Demo Configuration
DEMO_CONFIG = {
    # Which demos to include
    'enabled_demos': [
        'color_test',
        'pixel_test', 
        'line_test',
        'rect_test',
        'spiral_demo',
        'animation_demo',
        'sine_wave_demo',
        'text_demo',
    ],
    
    # Demo timing
    'demo_duration': 5000,  # 5 seconds per demo
    'demo_transition_time': 500,  # 0.5 second transition
    
    # Demo parameters
    'animation_speed': 1.0,  # Animation speed multiplier
    'color_cycling_speed': 1.0,
    'particle_count': 50,
}

# Advanced Features
ADVANCED_CONFIG = {
    # WiFi configuration (if enabled)
    'wifi_enabled': False,
    'wifi_ssid': '',
    'wifi_password': '',
    'wifi_timeout': 10000,
    
    # OTA update support
    'ota_enabled': False,
    'ota_url': '',
    
    # Data logging
    'logging_enabled': False,
    'log_to_file': False,
    'log_level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    
    # Custom extensions
    'extension_path': '/extensions',
    'auto_load_extensions': True,
}

def get_config(section=None):
    """Get configuration section or all configurations
    
    Args:
        section: Configuration section name or None for all
        
    Returns:
        Configuration dictionary
    """
    configs = {
        'display': DISPLAY_CONFIG,
        'ui': UI_CONFIG,
        'app': APP_CONFIG,
        'hardware': HARDWARE_CONFIG,
        'demo': DEMO_CONFIG,
        'advanced': ADVANCED_CONFIG,
    }
    
    if section is None:
        return configs
    
    return configs.get(section, {})

def validate_config():
    """Validate configuration values"""
    errors = []
    
    # Validate display config
    if not 0 <= DISPLAY_CONFIG['rotation'] <= 3:
        errors.append("Display rotation must be 0-3")
    
    if not 1000000 <= DISPLAY_CONFIG['spi_frequency'] <= 80000000:
        errors.append("SPI frequency must be between 1MHz and 80MHz")
    
    # Validate UI config
    if not 1 <= UI_CONFIG['animation_fps'] <= 60:
        errors.append("Animation FPS must be between 1 and 60")
    
    # Validate hardware config
    pins = HARDWARE_CONFIG['pins']
    pin_values = list(pins.values())
    if len(pin_values) != len(set(pin_values)):
        errors.append("Pin assignments must be unique")
    
    # Validate frequency
    freq = HARDWARE_CONFIG['cpu_frequency']
    if freq not in [80000000, 160000000, 240000000]:
        errors.append("CPU frequency must be 80, 160, or 240 MHz")
    
    return errors

def apply_config(board_config, display, ui):
    """Apply configuration to hardware and software components
    
    Args:
        board_config: BoardConfig instance
        display: ST7735Display instance  
        ui: LVGLUI instance
    """
    try:
        # Apply display configuration
        if DISPLAY_CONFIG['backlight_pwm']:
            # Configure PWM backlight if supported
            pass
        
        # Apply UI configuration
        if hasattr(ui, 'set_animation_fps'):
            ui.set_animation_fps(UI_CONFIG['animation_fps'])
        
        # Apply hardware configuration
        if HARDWARE_CONFIG['low_power_mode']:
            # Configure low power mode
            pass
        
        print("Configuration applied successfully")
        
    except Exception as e:
        print(f"Error applying configuration: {e}")

def save_config_to_file(filename='user_config.py'):
    """Save current configuration to file"""
    try:
        with open(filename, 'w') as f:
            f.write("# User configuration overrides\n")
            f.write("# This file is auto-generated\n\n")
            
            for section_name, section_config in get_config().items():
                f.write(f"# {section_name.upper()} Configuration\n")
                f.write(f"{section_name.upper()}_CONFIG = {section_config}\n\n")
        
        print(f"Configuration saved to {filename}")
        
    except Exception as e:
        print(f"Error saving configuration: {e}")

def load_config_from_file(filename='user_config.py'):
    """Load configuration from file"""
    try:
        # This would need to be implemented based on requirements
        # For now, just return current config
        return get_config()
        
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return get_config()

# Validate configuration on import
_validation_errors = validate_config()
if _validation_errors:
    print("Configuration validation errors:")
    for error in _validation_errors:
        print(f"  - {error}")
else:
    print("Configuration validated successfully")