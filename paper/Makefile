# The paper: `make` builds build/main.pdf, dated by the last commit so that the same sources give the same PDF;
# `make check` runs the structure, citation and claim checks and the prose lint; `make figures` regenerates the figures from paper/data/ (`make data` re-extracts the data first).
PYTHON ?= python3

.PHONY: all pdf check lint figures data clean

all: pdf

pdf:
	mkdir -p build
	SOURCE_DATE_EPOCH=$$(git log -1 --format=%ct) FORCE_SOURCE_DATE=1 \
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex >build/latexmk.out 2>&1 || (tail -40 build/latexmk.out; exit 1)
	@sha256sum build/main.pdf

check:
	$(PYTHON) tools/check.py

lint:
	$(PYTHON) tools/lint.py

figures:
	cd figures && $(PYTHON) figures.py

data:
	$(PYTHON) figures/extract.py

clean:
	rm -rf build
