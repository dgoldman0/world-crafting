# Every check: `make check`. Each target also runs on its own.
PYTHON ?= python3
export OPENBLAS_NUM_THREADS ?= 1

.PHONY: check check-patches test-python paper

check: check-patches test-python

# Each patch series applied to its pinned upstream source reproduces the deployed sources (upstream/ is
# ignored by Git; see models/pins.sha256 for what it must hold).
check-patches:
	models/check_patches.sh

# The in-house tools' tests (numba for the sky solver's; the spectroscopic inputs for ten of them).
test-python:
	$(PYTHON) -m pytest -q

# The paper's PDF, built in paper/build/ (paper/Makefile has its checks and figure targets).
paper:
	$(MAKE) -C paper pdf
