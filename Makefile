

.PHONY: all mrproper rebuild get-esp get-lvmicropython link-board-port build-spotpear-cross build-spotpear-%


# UART port for flashing/monitoring; note: you need dialup group or root access
PORT ?= /dev/ttyACM0

# Obtain specific supported tool
get-esp:
	git clone --recursive https://github.com/espressif/esp-idf.git -b v5.2.2
	(cd esp-idf ; git submodule update --init --recursive)
	(cd esp-idf ; ./install.sh )
	#(cd esp-idf ; git checkout v5.2.2 ; git submodule update --init --recursive)

#
get-lvmicropython:
	git clone https://github.com/lvgl/lv_micropython.git
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

build-spotpear-%:
	(cd lv_micropython ; source ../esp-idf/export.sh ; 					\
		make -C ports/esp32 BOARD=SPOTPEARC3 PORT=$(PORT) $*				\
	)



# Meta rules
setup:  get-esp get-lvmicropython link-board-port build-spotpear-cross

clean:
	@echo "Running clean that might fail if theres no product - not an issue."
	-$(MAKE) -C lv_micropython/ports/esp32  BOARD=SPOTPEARC3 clean

all: setup build-spotpear-submodules clean build-spotpear-all build-spotpear-deploy build-spotpear-monitor

rebuild: clean build-spotpear-all build-spotpear-deploy build-spotpear-monitor

mrproper:
	@rm -rf esp-idf lv_micropython
