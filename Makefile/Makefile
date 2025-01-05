PYTHON = python 
comp_dir = utils 
test_dir = tests
test_files = $(test_dir)/check_form.py
GENERER = generer.py
grammaires = $(test_dir)/grammaire1chomsky $(test_dir)/grammaire1.gegeral $(test_dir)/grammaire1.greibach

.PHONY: all test clean run 

all: test

test:
	@echo "Tests en cours d'execution"
	@$(PYTHON) $(test_files)
run:
	@echo "Fichier générer en cours d'execution"
	@$(PYTHON) $(GENERER)


