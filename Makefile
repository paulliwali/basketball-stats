.PHONY: setup install clean

VENV_PATH = .venv
PYTHON_VERSION = 3.11

setup:
	uv venv $(VENV_PATH) --python=$(PYTHON_VERSION)

install:
	. $(VENV_PATH)/bin/activate
	uv pip install .

clean:
	rm -rf $(VENV_PATH)

reinstall: clean setup install