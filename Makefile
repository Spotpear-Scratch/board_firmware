

.PHONY: all mrproper rebuild get-esp get-lvmicropython link-board-port build-spotpear-cross build-spotpear-submodules build-spotpear-build build-spotpear-deploy build-spotpear-monitor 

# UART port for flashing/monitoring; note: you need dialup group or root access
PORT ?= /dev/ttyACM0

# Obtain specific supported tool
get-esp:
	git clone --recursive https://github.com/espressif/esp-idf.git -v v5.2.2
	(cd esp-idf ; git submodule update --init --recursive)
	(cd esp-idf ; ./install.sh )
	#(cd esp-idf ; git checkout v5.2.2 ; git submodule update --init --recursive)

#
get-lvmicropython:
	git clone https://github.com/lvgl/lv_micropython.git
	(cd lv_micropython ; git submodule update --init --recursive user_modules/lv_binding_micropython)

#
link-board-port:
	ln -s lv_micropython_board_port/ports/esp32/boards/SPOTPEARC3 lv_micropython/ports/esp32/boards/SPOTPEARC3

#
build-spotpear-cross:
	(cd lv_micropython ; source ../esp-idf/export.sh ; 					\
		make -C mpy-cross						 						\
	)

build-spotpear-submodules:
	(cd lv_micropython ; source ../esp-idf/export.sh ; 					\
		make -C ports/esp32 BOARD=SPOTBEARC3 submodules					\
	)

build-spotpear-build:
	(cd lv_micropython ; source ../esp-idf/export.sh ; 					\
		make -C ports/esp32 BOARD=SPOTBEARC3 clean all					\
	)

build-spotpear-deploy:
	(cd lv_micropython ; source ../esp-idf/export.sh ; 					\
		make -C ports/esp32 BOARD=SPOTBEARC3 PORT=$(PORT) deploy		\
	)

build-spotpear-monitor:
	(cd lv_micropython ; source ../esp-idf/export.sh ; 					\
		make -C ports/esp32 BOARD=SPOTBEARC3 PORT=$(PORT) monitor		\
	)


# Meta rules
setup:  get-esp get-lvmicropython link-board-port build-spotpear-cross

all: setup build-spotpear-submodules build-spotpear-build build-spotpear-deploy build-spotpear-monitor

rebuild: build-spotpear-build build-spotpear-deploy build-spotpear-monitor

mrproper:
	@rm -rf esp-idf lv_micropython