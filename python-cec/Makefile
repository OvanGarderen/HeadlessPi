all: cec.so

ARCH:=$(shell uname -m)
SYS:=$(shell uname -s | tr '[:upper:]' '[:lower:]')
PY_VER:=$(shell python -c 'import sys; print("%d.%d"%(sys.version_info.major, sys.version_info.minor));')
ABI_VER:=$(shell python -c 'import sysconfig; print(sysconfig.get_config_var("SO"))')

BUILD_DIR:=build/lib.$(SYS)-$(ARCH)-$(PY_VER)

cec.so: $(BUILD_DIR)/cec$(ABI_VER)
	cp $< $@

$(BUILD_DIR)/cec$(ABI_VER): cec.cpp setup.py device.h device.cpp
	python setup.py build

test: all
	./test.py
.PHONY: test

clean:
	rm -rf build
	rm -f cec.so
.PHONY: clean
