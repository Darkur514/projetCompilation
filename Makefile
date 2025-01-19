PYTHON = python3
setup ?= default

test_general = test1.general
test_chomsky = test1.chomsky
test_greibach = test1.greibach
test_dir = custom_tests

.default_goal := all

setup:
	@echo "Setting up environment with: $(setup)"
	$(PYTHON) -m pip install $(setup)
	
clean:
	rm -rf __pycache__ utils/__pycache__

all: setup test compare

test:
	$(PYTHON) grammaire.py $(test_dir)/$(test_general)
	$(PYTHON) generer.py 4 $(test_dir)/$(test_chomsky) > $(test_dir)/test_4_chomsky.res
	$(PYTHON) generer.py 4 $(test_dir)/$(test_greibach) > $(test_dir)/test_4_greibach.res

compare:
	diff $(test_dir)/test_4_chomsky.res $(test_dir)/test_4_greibach.res

.PHONY: all setup test compare clean
