set(IDF_TARGET esp32c3)

set(SDKCONFIG_DEFAULTS
    boards/sdkconfig.base
    ${SDKCONFIG_IDF_VERSION_SPECIFIC}
    boards/sdkconfig.ble
    boards/SPOTPEARC3/sdkconfig.c3usb
)

set(MICROPY_FROZEN_MANIFEST ${MICROPY_BOARD_DIR}/manifest.py)

set(LV_CFLAGS -DLV_COLOR_DEPTH=16 -DLV_COLOR_16_SWAP=1)