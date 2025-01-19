PYTHON = python3
setup ?= default

grammar_file = test1
test_dir = custom_tests
len_mots = 4

.default_goal := all

# setup:
# 	@echo "Setting up environment with: $(setup)"
# 	$(PYTHON) -m pip install $(setup)
	
clean:
	rm -rf __pycache__ utils/__pycache__

all: setup test compare

test:
	$(PYTHON) grammaire.py $(test_dir)/$(grammar_file).general
	$(PYTHON) generer.py $(len_mots) $(test_dir)/$(grammar_file).chomsky > $(test_dir)/test_$(len_mots)_chomsky.res
	$(PYTHON) generer.py $(len_mots) $(test_dir)/$(grammar_file).greibach > $(test_dir)/test_$(len_mots)_greibach.res

compare:
	diff $(test_dir)/test_$(len_mots)_chomsky.res $(test_dir)/test_$(len_mots)_greibach.res

.PHONY: all setup test compare clean
