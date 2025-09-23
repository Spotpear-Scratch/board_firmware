# Read More here: docs/reference/manifest.rst

# Include other manifests
include("$(PORT_DIR)/boards/manifest.py")
include("$(MPY_DIR)/user_modules/lv_binding_micropython/ports/esp32")

# Add specific driver: Fixed up for (128,128) resolution, now inclulded in modules
#module("st77xx.py", base_path="$(MPY_DIR)/user_modules/lv_binding_micropython/driver/generic")
#

# Modules for ESP32C3 1.44 MiniTV
freeze("./modules")
