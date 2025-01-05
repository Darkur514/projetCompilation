PYTHON = python3
setup ?= default

test_general = tests/grammaire1.general
test_chomsky = tests/grammaire1.chomsky
test_greibach = tests/grammaire1.greibach

.PHONY: all test compare

all: test compare

test:
	$(PYTHON) grammaire.py $(test_general)
	$(PYTHON) generer.py 4 $(test_chomsky) > tests/test_4_chomsky.res
	$(PYTHON) generer.py 4 $(test_greibach) > tests/test_4_greibach.res

compare:
	diff tests/test_4_chomsky.res tests/test_4_greibach.res

setup:
	@echo "Setting up environment with: $(setup)"
	$(PYTHON) -m pip3 install $(setup)


