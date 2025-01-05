PYTHON = python3
setup ?= default

test_general = grammaire1.general
test_chomsky = grammaire1.chomsky
test_greibach = grammaire1.greibach
test_dir = tests

.default_goal := all

setup: pip install os sys copy

clean: rm -rf __pycache__ utils/__pycache__

all: setup test compare

test:
	$(PYTHON) grammaire.py $(test_dir)/$(test_general)
	$(PYTHON) generer.py 4 $(test_dir)/$(test_chomsky) > $(test_dir)/test_4_chomsky.res
	$(PYTHON) generer.py 4 $(test_dir)/$(test_greibach) > $(test_dir)/test_4_greibach.res

compare:
	diff $(test_dir)/test_4_chomsky.res $(test_dir)/test_4_greibach.res

.PHONY: all setup test compare clean



setup:
	@echo "Setting up environment with: $(setup)"
	$(PYTHON) -m pip3 install $(setup)


