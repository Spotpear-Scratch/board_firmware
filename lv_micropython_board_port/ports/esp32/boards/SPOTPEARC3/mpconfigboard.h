#define MICROPY_HW_BOARD_NAME "Spotpear C3-1.44 MiniTV"
#define MICROPY_HW_MCU_NAME "ESP32C3"

#define MICROPY_HW_ENABLE_SDCARD            (0)
#define MICROPY_PY_MACHINE_I2S              (0)

// LCD : ST7735 : https://github.com/Spotpear/ESP32C3_1.44inch/blob/main/miniapp/TFT_eSPI/User_Setup.h
//#define TFT_CS   PIN_D8  // Chip select control pin D8
//#define TFT_DC   PIN_D3  // Data Command control pin
//#define TFT_RST  PIN_D4  // Reset pin (could connect to NodeMCU RST, see next line)
//#define TFT_RST  -1    // Set TFT_RST to -1 if the display RESET is connected to NodeMC
//#define TFT_MOSI  4   // 1.90 4  1.44  4
//#define TFT_SCLK  3 // 1.90 11   1.44  3
//#define TFT_CS    2  // Chip select control pin  1.90 12  1.44 2
//#define TFT_DC    0 // Data Command control pin   1.90 7  1.44 0
//#define TFT_RST   5  // Reset pin (could connect to RST pin)  1.99 13  1.44 5
