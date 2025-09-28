# Read More here: docs/reference/manifest.rst

# Initial boot script to mount vfs, and remove main.py if buttons are down
module("_boot.py", opt=3)

# Include other manifests
#include("$(PORT_DIR)/boards/manifest.py")

include("$(MPY_DIR)/user_modules/lv_binding_micropython/ports/esp32")

# NOTE: Cannot use original as it needs fixes up for (128,128) resolution, now inclulded in modules folder
#module("st77xx.py", base_path="$(MPY_DIR)/user_modules/lv_binding_micropython/driver/generic")
#

# Modules for ESP32C3 1.44 MiniTV
freeze("./modules")

# Coming from originally #include("$(PORT_DIR)/boards/manifest.py")
# however due to it containing _boot.py we had to copy the relevant parts into
# modules folder and freeze it here.


include("$(MPY_DIR)/extmod/asyncio")

# Useful networking-related packages.
require("bundle-networking")

# Require some micropython-lib modules.
require("aioespnow")
require("dht")
require("ds18x20")
require("neopixel")
require("onewire")
require("umqtt.robust")
require("umqtt.simple")
require("upysh")

