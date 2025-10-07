

.PHONY: get-esp get-lvmicropython all mrproper rebuild get-esp get-lvmicropython link-board-port build-spotpear-cross build-spotpear-%


# UART port for flashing/monitoring; note: you need dialup group or root access
PORT ?= /dev/ttyACM0

# Obtain specific supported tool
get-esp:
	if [ ! -d esp-idf ] ; then git clone --recursive https://github.com/espressif/esp-idf.git -b v5.2.2 ; fi
	if [ ! "$(shell cd esp-idf ; git describe --tags --exact-match 2>/dev/null || echo 'x')" == "v5.2.2" ] ; then echo "Not on tag v5.2.2 or esp-idf folder is corrupt, remove and start again" ; exit 1 ; fi
	(cd esp-idf ; git submodule update --init --recursive)
	(cd esp-idf ; ./install.sh )

# Obtain specific supported lv_micropython
get-lvmicropython:
	if [ ! -d lv_micropython ] ; then git clone https://github.com/lvgl/lv_micropython.git ; fi
	(cd lv_micropython ; git submodule update --init --recursive user_modules/lv_binding_micropython)

#
link-board-port:
	ln -s $(shell readlink -m lv_micropython_board_port/ports/esp32/boards/SPOTPEARC3) lv_micropython/ports/esp32/boards/SPOTPEARC3

#
build-spotpear-cross:
	(cd lv_micropython ; source ../esp-idf/export.sh ; 					\
		make -C mpy-cross						 						\
	)

build-spotpear-submodules:
	(cd lv_micropython ; source ../esp-idf/export.sh ; 					\
		make -C ports/esp32 BOARD=SPOTPEARC3 submodules					\
	)

build-spotpear-clean:
	(cd lv_micropython ; source ../esp-idf/export.sh ; 					\
		make -C ports/esp32 BOARD=SPOTPEARC3 PORT=$(PORT) clean				\
	)

SHA := $(shell git rev-parse --short=10 HEAD)
build-spotpear-tagmachinename:
	(cd lv_micropython_board_port/ports/esp32/boards/SPOTPEARC3 ; 				\
		sed -i 's/\(version \)[^)]*/\1'"$(SHA)"'/' mpconfigboard.h 				\
	)


build-spotpear-%:
	(cd lv_micropython ; source ../esp-idf/export.sh ; 					\
		make -C ports/esp32 BOARD=SPOTPEARC3 PORT=$(PORT) $*				\
	)



# Meta rules
setup:  get-esp get-lvmicropython link-board-port build-spotpear-cross


clean:
	@echo "Running clean that might fail if theres no product - not an issue."
	-(source esp-idf/export.sh ; $(MAKE) -C lv_micropython/ports/esp32  BOARD=SPOTPEARC3 clean)


rebuild: clean build-spotpear-tagmachinename build-spotpear-all build-spotpear-deploy build-spotpear-monitor


all: setup build-spotpear-submodules rebuild


mrproper:
	@rm -rf esp-idf lv_micropython
